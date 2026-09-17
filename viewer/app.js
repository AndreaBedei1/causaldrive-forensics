/* CDF forensic viewer -- static, dependency-free renderer for run_data.json.
 *
 * Contract with the bundle (src/cdf/viewer/bundle.py):
 *   - everything privileged lives under data.oracle and nowhere else, so the
 *     ORACLE perspective is the only code path that reads that key. A local
 *     perspective can only reach data.participants[pid]; there is no branch that
 *     mixes them, which is the whole point of the split.
 *   - blocks whose artifacts were missing are absent and listed in data.notes.
 *     Every panel therefore renders "not available for this run" rather than an
 *     empty chart.
 *
 * No framework, no bundler, no network: the page is opened from a run directory
 * that may be on an offline machine. SVG is produced as markup strings and
 * handed to innerHTML on plain <div> containers -- the HTML parser puts the
 * children in the SVG namespace for us, which keeps this file free of any
 * namespace URI or DOM-construction boilerplate.
 */
(function () {
  'use strict';

  // ------------------------------------------------------------------ state

  var DATA = null;          // the parsed bundle
  var VIEW = null;          // the derived view model for the active perspective
  var T = 0;                // current timeline position, simulation seconds
  var PLAYING = false;
  var LAST_FRAME = 0;       // performance.now() of the previous animation frame
  var SELECTED = null;      // selected causal-graph node id
  var HIGHLIGHT = { nodes: {}, edges: {} };

  var OUTCOME_TYPES = { COLLISION: 1, NEAR_MISS: 1, POST_IMPACT_STOP: 1 };
  var VEHICLE_L = 4.6;      // metres, drawn footprint only
  var VEHICLE_W = 2.0;
  var PARTICIPANT_COLORS = ['--p-a', '--p-b', '--p-c', '--p-d', '--p-e'];

  var el = {};

  // ---------------------------------------------------------------- helpers

  function $(id) { return document.getElementById(id); }

  function esc(s) {
    return String(s === null || s === undefined ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function num(v, digits) {
    if (v === null || v === undefined || typeof v !== 'number' || !isFinite(v)) return '--';
    return v.toFixed(digits === undefined ? 2 : digits);
  }

  function cssVar(name) {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  }

  function participantColor(pid) {
    var ids = (DATA && DATA.run && DATA.run.participant_ids) || [];
    var i = ids.indexOf(pid);
    if (i < 0) i = Math.abs(String(pid).charCodeAt(0)) % PARTICIPANT_COLORS.length;
    return cssVar(PARTICIPANT_COLORS[i % PARTICIPANT_COLORS.length]);
  }

  function provenanceColor(prov) {
    if (prov === 'oracle') return cssVar('--oracle');
    if (prov === 'fused') return cssVar('--fused');
    return cssVar('--local');
  }

  /* Interpolated sample of a time series at time t, or null when t lies outside
   * the recorded span. Returning null (rather than clamping) matters: a vehicle
   * that was not recording at t must not be drawn as if it were. */
  function sampleAt(points, t) {
    if (!points || points.length === 0) return null;
    var eps = 1e-6;
    if (t < points[0].t - eps || t > points[points.length - 1].t + eps) return null;
    var lo = 0, hi = points.length - 1;
    while (lo < hi - 1) {
      var mid = (lo + hi) >> 1;
      if (points[mid].t <= t) lo = mid; else hi = mid;
    }
    var a = points[lo], b = points[hi];
    var span = b.t - a.t;
    var f = span > eps ? (t - a.t) / span : 0;
    var out = {};
    for (var k in a) {
      if (!Object.prototype.hasOwnProperty.call(a, k)) continue;
      var va = a[k], vb = b[k];
      if (typeof va !== 'number' || typeof vb !== 'number') { out[k] = va; continue; }
      out[k] = k === 'yaw' ? lerpAngle(va, vb, f) : va + (vb - va) * f;
    }
    return out;
  }

  function lerpAngle(a, b, f) {
    var d = ((b - a + 540) % 360) - 180;   // shortest way round
    return a + d * f;
  }

  function clamp(v, lo, hi) { return v < lo ? lo : (v > hi ? hi : v); }

  function runSpan() {
    var r = DATA.run || {};
    var t0 = typeof r.t_start === 'number' ? r.t_start : 0;
    var t1 = typeof r.t_end === 'number' ? r.t_end : t0 + 1;
    if (t1 <= t0) t1 = t0 + 1;
    return [t0, t1];
  }

  /* Short human description of an event's measured values, e.g. "ttc_s 0.45". */
  function valueSummary(values) {
    if (!values) return '';
    var parts = [];
    Object.keys(values).sort().forEach(function (k) {
      var v = values[k];
      parts.push(k + ' ' + (typeof v === 'number' ? num(v, 2) : esc(v)));
    });
    return parts.join(', ');
  }

  // ------------------------------------------------------------------- boot

  function boot() {
    ['banner', 'run-title', 'run-meta', 'perspectives', 'app', 'map', 'map-source',
     'map-legend', 'time', 'play', 'clock', 'signals', 'signals-source', 'events',
     'graph', 'graph-detail', 'checking', 'identity', 'attribution', 'notes'
    ].forEach(function (id) { el[id] = $(id); });

    fetch('run_data.json')
      .then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status + ' ' + r.statusText);
        return r.json();
      })
      .then(function (json) { DATA = json; start(); })
      .catch(fatal);
  }

  /* A failed fetch is nearly always the browser's file:// restriction rather
   * than a missing file, so say exactly how to get past it instead of printing
   * a bare stack trace. */
  function fatal(err) {
    var msg = (err && err.message) ? err.message : String(err);
    document.body.innerHTML =
      '<div id="fatal"><h2>Could not load run_data.json</h2>' +
      '<p>' + esc(msg) + '</p>' +
      '<p>The page fetches <code>run_data.json</code> from its own directory. ' +
      'Browsers refuse that over <code>file://</code>, so serve the run directory ' +
      'over HTTP from a terminal:</p>' +
      '<pre>cd &lt;run_dir&gt;/viewer\npython -m http.server 8000\n' +
      '# then open localhost:8000/index.html in the browser</pre>' +
      '<p>If the file really is absent, regenerate it with ' +
      '<code>cdf.viewer.bundle.write_bundle(run_dir, cfg)</code>.</p></div>';
  }

  function start() {
    var span = runSpan();
    T = span[0];
    el.app.hidden = false;
    renderHeader();
    buildPerspectiveButtons();
    setPerspective(defaultPerspective());
    renderNotes();
    wireTransport();
    window.addEventListener('resize', drawMap);
  }

  function defaultPerspective() {
    var ids = (DATA.run && DATA.run.participant_ids) || [];
    return ids.length ? ids[0] : (DATA.fusion ? 'FUSED' : 'ORACLE');
  }

  function renderHeader() {
    var r = DATA.run || {};
    el['run-title'].textContent =
      (r.run_id || r.run_dir || 'run') + '  --  ' + (r.scenario_id || '?') +
      (r.variant ? ' / ' + r.variant : '');
    el['run-meta'].textContent =
      'map ' + (r.map || '?') + '  |  seed ' + (r.seed === null ? '?' : r.seed) +
      '  |  outcome ' + (r.outcome || 'unknown') +
      '  |  ' + num(r.duration_s, 2) + ' s @ dt ' + num(r.dt, 3) + ' s' +
      '  |  config ' + (r.config_hash || '?');
  }

  function buildPerspectiveButtons() {
    var html = '';
    (DATA.run.participant_ids || []).forEach(function (pid) {
      html += '<button class="pbtn" type="button" data-view="' + esc(pid) +
              '" data-kind="local">' + esc(pid) + '</button>';
    });
    if (DATA.fusion) {
      html += '<button class="pbtn" type="button" data-view="FUSED" data-kind="fused">FUSED</button>';
    }
    if (DATA.oracle) {
      html += '<button class="pbtn" type="button" data-view="ORACLE" data-kind="oracle">ORACLE</button>';
    }
    el.perspectives.innerHTML = html;
    el.perspectives.addEventListener('click', function (ev) {
      var btn = ev.target.closest('.pbtn');
      if (btn) setPerspective(btn.getAttribute('data-view'));
    });
  }

  // ------------------------------------------------------------ view model

  /* Build everything the panels need for one perspective.
   *
   * This is the single place where a perspective decides which part of the
   * bundle it may read. A local view is given the participant's own telemetry
   * and its own tracks and nothing else; the fused view is given the
   * participants' exchanged logs plus the fused graph; the oracle view is the
   * only one that ever touches DATA.oracle. */
  function buildView(id) {
    if (id === 'ORACLE') return buildOracleView();
    if (id === 'FUSED') return buildFusedView();
    return buildLocalView(id);
  }

  function buildLocalView(pid) {
    var p = DATA.participants[pid];
    var tracks = [];
    Object.keys(p.tracks || {}).sort().forEach(function (tid) {
      tracks.push({ track_id: tid, observer: pid, points: p.tracks[tid] });
    });
    return {
      id: pid, kind: 'local',
      badge: 'LOCAL RECONSTRUCTION',
      sub: 'vehicle ' + pid + ' -- own telemetry, own controls, own radar tracks only. ' +
           'No other participant\'s trajectory appears in this view.',
      trajectories: [{ pid: pid, label: pid + ' (own telemetry)', points: p.telemetry || [] }],
      tracks: tracks,
      events: (p.events || []).slice(),
      controls: p.controls || [],
      causal: p.causal_graph || null,
      causalLabel: 'local causal DAG of ' + pid,
      missingCausal: 'no local causal graph was persisted for ' + pid
    };
  }

  function buildFusedView() {
    var trajectories = [];
    (DATA.run.participant_ids || []).forEach(function (pid) {
      var p = DATA.participants[pid];
      if (p && p.telemetry && p.telemetry.length) {
        trajectories.push({ pid: pid, label: pid + ' (exchanged log)', points: p.telemetry });
      }
    });
    var nodes = (DATA.fusion.causal_graph && DATA.fusion.causal_graph.nodes) || [];
    return {
      id: 'FUSED', kind: 'fused',
      badge: 'FUSED RECONSTRUCTION',
      sub: 'independent local reconstructions merged from exchanged logs and ' +
           'trajectory evidence. Identities are inferred, not given.',
      trajectories: trajectories,
      tracks: [],
      events: nodes.slice(),
      controls: [],
      causal: DATA.fusion.causal_graph || null,
      causalLabel: 'fused causal DAG',
      missingCausal: 'no fused causal graph in this run'
    };
  }

  function buildOracleView() {
    var trajectories = [];
    Object.keys(DATA.oracle.trajectories || {}).sort().forEach(function (pid) {
      trajectories.push({ pid: pid, label: pid + ' (ground truth)', points: DATA.oracle.trajectories[pid] });
    });
    return {
      id: 'ORACLE', kind: 'oracle',
      badge: DATA.oracle._warning || 'PRIVILEGED GROUND TRUTH - EVALUATION ONLY',
      sub: 'simulator ground truth. Never used by any reconstruction; shown here ' +
           'only so a reconstruction can be scored against it.',
      trajectories: trajectories,
      tracks: [],
      events: (DATA.oracle.events || []).slice(),
      controls: [],
      causal: DATA.oracle.causal_graph || null,
      causalLabel: 'oracle causal DAG',
      missingCausal: 'no oracle causal graph in this run'
    };
  }

  function setPerspective(id) {
    VIEW = buildView(id);
    SELECTED = null;
    HIGHLIGHT = { nodes: {}, edges: {} };
    document.body.setAttribute('data-perspective', VIEW.kind === 'local' ? 'LOCAL' : VIEW.id);
    el.banner.innerHTML = esc(VIEW.badge) + '<span class="sub">' + esc(VIEW.sub) + '</span>';
    Array.prototype.forEach.call(el.perspectives.querySelectorAll('.pbtn'), function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-view') === id ? 'true' : 'false');
    });
    VIEW.bounds = null;
    renderSignals();
    renderEvents();
    renderGraph();
    renderChecking();
    renderIdentity();
    renderAttribution();
    drawMap();
    tick(T);
  }

  // -------------------------------------------------------------- transport

  function wireTransport() {
    var span = runSpan();
    el.time.min = String(span[0]);
    el.time.max = String(span[1]);
    el.time.step = String(Math.max(0.01, (DATA.run.dt || 0.05) / 2));
    el.time.value = String(T);
    el.time.addEventListener('input', function () { pause(); tick(parseFloat(el.time.value)); });
    el.play.addEventListener('click', function () { PLAYING ? pause() : play(); });
    document.addEventListener('keydown', function (ev) {
      if (ev.target && /input|textarea/i.test(ev.target.tagName)) return;
      if (ev.code === 'Space') { ev.preventDefault(); PLAYING ? pause() : play(); }
      else if (ev.code === 'ArrowRight') { pause(); tick(T + (DATA.run.dt || 0.05)); }
      else if (ev.code === 'ArrowLeft') { pause(); tick(T - (DATA.run.dt || 0.05)); }
    });
  }

  function play() {
    var span = runSpan();
    if (T >= span[1] - 1e-6) T = span[0];
    PLAYING = true;
    el.play.textContent = 'Pause';
    LAST_FRAME = performance.now();
    requestAnimationFrame(frame);
  }

  function pause() {
    PLAYING = false;
    el.play.textContent = 'Play';
  }

  /* Playback runs at 1x simulation time, driven by the wall clock delta rather
   * than a fixed increment, so the animation keeps real-time meaning on a slow
   * machine instead of silently running in slow motion. */
  function frame(now) {
    if (!PLAYING) return;
    var dt = (now - LAST_FRAME) / 1000;
    LAST_FRAME = now;
    var span = runSpan();
    var next = T + dt;
    if (next >= span[1]) { tick(span[1]); pause(); return; }
    tick(next);
    requestAnimationFrame(frame);
  }

  function seek(t) { pause(); tick(t); }

  function tick(t) {
    var span = runSpan();
    T = clamp(t, span[0], span[1]);
    el.time.value = String(T);
    el.clock.textContent = 't = ' + num(T, 2) + ' s';
    drawMap();
    updateSignalCursors();
    updateEventHighlight();
  }

  // --------------------------------------------------------------- map view

  function collectBounds() {
    var xs = [], ys = [];
    VIEW.trajectories.forEach(function (tr) {
      tr.points.forEach(function (p) { xs.push(p.x); ys.push(p.y); });
    });
    VIEW.tracks.forEach(function (tr) {
      tr.points.forEach(function (p) { xs.push(p.gx); ys.push(p.gy); });
    });
    conflictRegions().forEach(function (c) { xs.push(c.x); ys.push(c.y); });
    if (!xs.length) return null;
    var b = {
      x0: Math.min.apply(null, xs), x1: Math.max.apply(null, xs),
      y0: Math.min.apply(null, ys), y1: Math.max.apply(null, ys)
    };
    // Never let a nearly-straight run collapse to a line: keep at least 30 m.
    var minSpan = 30;
    if (b.x1 - b.x0 < minSpan) { var cx = (b.x0 + b.x1) / 2; b.x0 = cx - minSpan / 2; b.x1 = cx + minSpan / 2; }
    if (b.y1 - b.y0 < minSpan) { var cy = (b.y0 + b.y1) / 2; b.y0 = cy - minSpan / 2; b.y1 = cy + minSpan / 2; }
    var padx = (b.x1 - b.x0) * 0.08, pady = (b.y1 - b.y0) * 0.08;
    b.x0 -= padx; b.x1 += padx; b.y0 -= pady; b.y1 += pady;
    return b;
  }

  /* Conflict regions are an inference the ego made about where the paths would
   * be contested; the centre travels in the event's own values. */
  function conflictRegions() {
    var out = [];
    (VIEW.events || []).forEach(function (e) {
      var v = e.values || {};
      if (typeof v.conflict_x === 'number' && typeof v.conflict_y === 'number') {
        out.push({
          x: v.conflict_x, y: v.conflict_y,
          t_start: e.t_start, t_end: e.t_end === null || e.t_end === undefined ? e.t_peak : e.t_end,
          label: e.event_type, subject: e.subject
        });
      }
    });
    return out;
  }

  function drawMap() {
    var cv = el.map;
    if (!cv || !VIEW) return;
    var dpr = window.devicePixelRatio || 1;
    var rect = cv.getBoundingClientRect();
    cv.width = Math.max(320, Math.round(rect.width * dpr));
    cv.height = Math.max(240, Math.round(rect.height * dpr));
    var g = cv.getContext('2d');
    g.setTransform(dpr, 0, 0, dpr, 0, 0);
    var W = rect.width, H = rect.height;
    g.clearRect(0, 0, W, H);

    if (!VIEW.bounds) VIEW.bounds = collectBounds();
    var b = VIEW.bounds;
    if (!b) {
      g.fillStyle = cssVar('--muted');
      g.font = '13px sans-serif';
      g.fillText('no geometry available for this perspective', 16, 28);
      el['map-source'].textContent = '';
      return;
    }

    // Uniform scale so distances on screen are comparable in both axes.
    var s = Math.min(W / (b.x1 - b.x0), H / (b.y1 - b.y0));
    var ox = (W - (b.x1 - b.x0) * s) / 2, oy = (H - (b.y1 - b.y0) * s) / 2;
    function sx(x) { return ox + (x - b.x0) * s; }
    function sy(y) { return oy + (y - b.y0) * s; }

    drawGrid(g, W, H, b, s, sx, sy);
    drawConflictRegions(g, sx, sy, s);
    drawTrajectories(g, sx, sy);
    drawTracks(g, sx, sy);
    drawEventMarkers(g, sx, sy);
    drawCollisions(g, sx, sy, s);
    drawVehicles(g, sx, sy, s);
    drawScaleBar(g, W, H, s);

    el['map-source'].textContent = '- ' + VIEW.trajectories.map(function (t) { return t.label; }).join(', ');
    renderLegend();
  }

  function drawGrid(g, W, H, b, s, sx, sy) {
    var step = 10;                                   // metres
    while ((step * s) < 40) step *= 2;
    g.strokeStyle = 'rgba(255,255,255,0.045)';
    g.lineWidth = 1;
    g.beginPath();
    for (var x = Math.ceil(b.x0 / step) * step; x <= b.x1; x += step) {
      g.moveTo(sx(x), 0); g.lineTo(sx(x), H);
    }
    for (var y = Math.ceil(b.y0 / step) * step; y <= b.y1; y += step) {
      g.moveTo(0, sy(y)); g.lineTo(W, sy(y));
    }
    g.stroke();
  }

  function drawTrajectories(g, sx, sy) {
    VIEW.trajectories.forEach(function (tr, idx) {
      var color = VIEW.kind === 'oracle' ? cssVar('--oracle') : participantColor(tr.pid);
      var pts = tr.points;
      if (!pts.length) return;
      g.save();
      // The oracle view is deliberately monochrome red; participants are told
      // apart by dash pattern so no ground-truth trace can read as a local one.
      if (VIEW.kind === 'oracle' && idx % 2 === 1) g.setLineDash([9, 5]);
      // Whole path, dim: the context of where the vehicle went.
      g.strokeStyle = color; g.globalAlpha = 0.25; g.lineWidth = 1.5;
      strokePolyline(g, pts, sx, sy, function (p) { return [p.x, p.y]; });
      // Travelled-so-far, solid: what has happened by the current time.
      g.globalAlpha = 0.95; g.lineWidth = 2.5;
      var travelled = pts.filter(function (p) { return p.t <= T + 1e-6; });
      strokePolyline(g, travelled, sx, sy, function (p) { return [p.x, p.y]; });
      g.globalAlpha = 1;
      g.restore();
    });
  }

  function strokePolyline(g, pts, sx, sy, get) {
    if (!pts || pts.length < 2) return;
    g.beginPath();
    for (var i = 0; i < pts.length; i++) {
      var c = get(pts[i]);
      var X = sx(c[0]), Y = sy(c[1]);
      if (i === 0) g.moveTo(X, Y); else g.lineTo(X, Y);
    }
    g.stroke();
  }

  /* Radar tracks are drawn in the observer's colour but dashed and translucent:
   * they are estimates of where something else was, never a measured pose. The
   * opacity of the current marker is the tracker's own confidence. */
  function drawTracks(g, sx, sy) {
    VIEW.tracks.forEach(function (tr) {
      var pts = tr.points || [];
      if (!pts.length) return;
      var meanConf = pts.reduce(function (a, p) { return a + (p.confidence || 0); }, 0) / pts.length;
      g.save();
      g.setLineDash([5, 4]);
      g.strokeStyle = cssVar('--fg');
      g.globalAlpha = 0.15 + 0.5 * clamp(meanConf, 0, 1);
      g.lineWidth = 1.5;
      strokePolyline(g, pts, sx, sy, function (p) { return [p.gx, p.gy]; });
      g.restore();

      var now = sampleAt(pts, T);
      if (now) {
        g.save();
        g.globalAlpha = clamp(0.2 + 0.8 * (now.confidence || 0), 0.2, 1);
        g.fillStyle = cssVar('--fg');
        g.beginPath();
        g.arc(sx(now.gx), sy(now.gy), 5, 0, Math.PI * 2);
        g.fill();
        g.globalAlpha = 1;
        g.fillStyle = cssVar('--fg');
        g.font = '11px Consolas, monospace';
        g.fillText(tr.track_id + '  ' + num(now.range_m, 1) + ' m' +
                   (typeof now.ttc === 'number' ? '  ttc ' + num(now.ttc, 2) + ' s' : '') +
                   '  conf ' + num(now.confidence, 2),
                   sx(now.gx) + 9, sy(now.gy) - 8);
        g.restore();
      }
    });
  }

  function drawConflictRegions(g, sx, sy, s) {
    var radius = (DATA.params && DATA.params.conflict_region_radius_m) || 6;
    conflictRegions().forEach(function (c) {
      var active = T >= c.t_start - 1e-6 && T <= c.t_end + 1e-6;
      g.save();
      g.setLineDash([4, 4]);
      g.strokeStyle = cssVar('--unknown');
      g.globalAlpha = active ? 0.85 : 0.22;
      g.lineWidth = active ? 2 : 1;
      g.beginPath();
      g.arc(sx(c.x), sy(c.y), radius * s, 0, Math.PI * 2);
      g.stroke();
      if (active) {
        g.setLineDash([]);
        g.fillStyle = cssVar('--unknown');
        g.font = '11px sans-serif';
        g.fillText('inferred conflict region', sx(c.x) + radius * s + 4, sy(c.y));
      }
      g.restore();
    });
  }

  /* Event markers sit where the vehicle that recorded the event was at the time
   * it recorded it, which is the only position the evidence supports. */
  function drawEventMarkers(g, sx, sy) {
    (VIEW.events || []).forEach(function (e) {
      var pos = positionOfParticipant(e.participant_id, e.t_peak);
      if (!pos) return;
      var near = Math.abs(e.t_peak - T) <= 0.75;
      var outcome = !!OUTCOME_TYPES[e.event_type];
      g.save();
      g.globalAlpha = near ? 1 : 0.35;
      g.fillStyle = outcome ? cssVar('--fail') : cssVar('--accent');
      g.beginPath();
      g.arc(sx(pos.x), sy(pos.y), near ? 4.5 : 2.5, 0, Math.PI * 2);
      g.fill();
      if (near) {
        g.fillStyle = cssVar('--fg');
        g.font = '11px sans-serif';
        g.fillText(e.event_type + ' @ ' + num(e.t_peak, 2) + ' s', sx(pos.x) + 7, sy(pos.y) + 12);
      }
      g.restore();
    });
  }

  /* Where the impact happened, as far as this perspective can tell:
   *   - local  : this vehicle's own position when its own COLLISION event fired
   *   - fused  : the position of every participant the fused graph says collided
   *   - oracle : the recorded true collision.
   * Nothing is inferred beyond reading the recorded time and looking up the
   * position that the same view already draws. */
  function drawCollisions(g, sx, sy, s) {
    var marks = [];
    if (VIEW.kind === 'oracle') {
      (DATA.oracle.collisions || []).forEach(function (c) {
        var pos = positionOfParticipant(c.participant_id, c.t);
        if (pos) marks.push({ x: pos.x, y: pos.y, t: c.t, label: 'collision ' + c.participant_id + '/' + (c.other_participant_id || '?') });
      });
    } else {
      (VIEW.events || []).forEach(function (e) {
        if (e.event_type !== 'COLLISION') return;
        var pos = positionOfParticipant(e.participant_id, e.t_peak);
        if (pos) marks.push({ x: pos.x, y: pos.y, t: e.t_peak, label: 'collision (' + e.participant_id + ')' });
      });
    }
    marks.forEach(function (m, idx) {
      g.save();
      g.strokeStyle = cssVar('--fail');
      g.lineWidth = 2.5;
      var X = sx(m.x), Y = sy(m.y), r = 9;
      g.beginPath();
      g.moveTo(X - r, Y - r); g.lineTo(X + r, Y + r);
      g.moveTo(X + r, Y - r); g.lineTo(X - r, Y + r);
      g.stroke();
      g.globalAlpha = 0.5;
      g.beginPath(); g.arc(X, Y, r + 5, 0, Math.PI * 2); g.stroke();
      g.globalAlpha = 1;
      g.fillStyle = cssVar('--fail');
      g.font = '11px sans-serif';
      g.fillText(m.label + ' @ ' + num(m.t, 2) + ' s', X + r + 8, Y + r + 14 + idx * 14);
      g.restore();
    });
  }

  function drawVehicles(g, sx, sy, s) {
    VIEW.trajectories.forEach(function (tr, idx) {
      var p = sampleAt(tr.points, T);
      if (!p) return;
      var color = VIEW.kind === 'oracle' ? cssVar('--oracle') : participantColor(tr.pid);
      var X = sx(p.x), Y = sy(p.y);
      // CARLA yaw is clockwise about the down axis, and screen y grows
      // downwards, so a plain rotation by +yaw points the box the right way.
      var a = (p.yaw || 0) * Math.PI / 180;
      g.save();
      g.translate(X, Y);
      g.rotate(a);
      g.fillStyle = color;
      g.globalAlpha = 0.85;
      g.fillRect(-VEHICLE_L * s / 2, -VEHICLE_W * s / 2, VEHICLE_L * s, VEHICLE_W * s);
      g.globalAlpha = 1;
      g.strokeStyle = '#000';
      g.lineWidth = 1;
      g.strokeRect(-VEHICLE_L * s / 2, -VEHICLE_W * s / 2, VEHICLE_L * s, VEHICLE_W * s);
      // Nose marker, so heading is readable even at small scale.
      g.fillStyle = '#000';
      g.fillRect(VEHICLE_L * s / 2 - 2, -1.5, 2, 3);
      g.restore();

      // Two vehicles at the moment of impact occupy the same pixel, so stagger
      // the labels by lane index instead of letting them overprint.
      g.fillStyle = color;
      g.font = 'bold 12px sans-serif';
      g.fillText(tr.pid + '  ' + num(p.speed, 1) + ' m/s', X + 12, Y - 10 - idx * 15);
    });
  }

  function drawScaleBar(g, W, H, s) {
    var metres = 10;
    while (metres * s < 60) metres *= 2;
    var px = metres * s;
    var x0 = W - px - 18, y0 = H - 18;
    g.strokeStyle = cssVar('--muted');
    g.lineWidth = 2;
    g.beginPath();
    g.moveTo(x0, y0); g.lineTo(x0 + px, y0);
    g.moveTo(x0, y0 - 4); g.lineTo(x0, y0 + 4);
    g.moveTo(x0 + px, y0 - 4); g.lineTo(x0 + px, y0 + 4);
    g.stroke();
    g.fillStyle = cssVar('--muted');
    g.font = '11px sans-serif';
    g.fillText(metres + ' m', x0 + px / 2 - 10, y0 - 6);
  }

  /* Position of a participant at time t *within the active perspective*. A local
   * view can only answer for its own vehicle -- that is the boundary, expressed
   * as code: there is simply no other trajectory in VIEW.trajectories. */
  function positionOfParticipant(pid, t) {
    for (var i = 0; i < VIEW.trajectories.length; i++) {
      if (VIEW.trajectories[i].pid === pid) return sampleAt(VIEW.trajectories[i].points, t);
    }
    return null;
  }

  function renderLegend() {
    var items = VIEW.trajectories.map(function (tr) {
      var c = VIEW.kind === 'oracle' ? cssVar('--oracle') : participantColor(tr.pid);
      return '<span class="key"><i class="swatch" style="background:' + c + '"></i>' + esc(tr.label) + '</span>';
    });
    if (VIEW.tracks.length) {
      items.push('<span class="key"><i class="swatch" style="background:' + cssVar('--fg') +
                 ';opacity:.6"></i>own radar tracks (opacity = confidence)</span>');
    }
    if (conflictRegions().length) {
      items.push('<span class="key"><i class="swatch" style="background:' + cssVar('--unknown') +
                 '"></i>inferred conflict region</span>');
    }
    items.push('<span class="key"><i class="swatch" style="background:' + cssVar('--fail') + '"></i>collision / outcome</span>');
    el['map-legend'].innerHTML = items.join('');
  }

  // ---------------------------------------------------------------- signals

  var PLOTS = [];   // [{key, el, cursor, valueEl, series, field}]

  /* One stacked strip chart per signal. The strips are built once per
   * perspective and only the cursor moves while the timeline runs, which keeps
   * scrubbing smooth without any charting library. */
  function renderSignals() {
    PLOTS = [];
    var span = runSpan();
    var specs = [];

    if (VIEW.kind === 'local') {
      var p = DATA.participants[VIEW.id];
      specs.push({ title: 'speed (m/s)', points: p.telemetry, field: 'speed', color: participantColor(VIEW.id) });
      specs.push({ title: 'accel_long (m/s^2)', points: p.telemetry, field: 'accel_long', color: participantColor(VIEW.id) });
      specs.push({ title: 'throttle', points: p.controls, field: 'throttle', color: cssVar('--pass'), fixed: [0, 1] });
      specs.push({ title: 'brake', points: p.controls, field: 'brake', color: cssVar('--fail'), fixed: [0, 1] });
      specs.push({ title: 'steer', points: p.controls, field: 'steer', color: cssVar('--unknown'), fixed: [-1, 1] });
      Object.keys(p.tracks || {}).sort().forEach(function (tid) {
        var pts = (p.tracks[tid] || []).filter(function (r) { return typeof r.ttc === 'number'; });
        if (pts.length > 1) {
          specs.push({ title: 'TTC ' + tid + ' (s)', points: pts, field: 'ttc', color: cssVar('--fused') });
        }
      });
      el['signals-source'].textContent = '- own telemetry, own controls, own radar';
    } else if (VIEW.kind === 'fused') {
      VIEW.trajectories.forEach(function (tr) {
        specs.push({ title: 'speed ' + tr.pid + ' (m/s)', points: tr.points, field: 'speed', color: participantColor(tr.pid) });
      });
      VIEW.trajectories.forEach(function (tr) {
        var ctl = (DATA.participants[tr.pid] || {}).controls || [];
        if (ctl.length) specs.push({ title: 'brake ' + tr.pid, points: ctl, field: 'brake', color: cssVar('--fail'), fixed: [0, 1] });
      });
      el['signals-source'].textContent = '- exchanged local logs, on the fusion reference clock';
    } else {
      VIEW.trajectories.forEach(function (tr) {
        specs.push({ title: 'speed ' + tr.pid + ' (m/s, true)', points: tr.points, field: 'speed', color: cssVar('--oracle') });
      });
      el['signals-source'].textContent = '- ground-truth state';
    }

    var html = '';
    specs.forEach(function (spec, i) {
      html += '<div class="plot" data-plot="' + i + '">' +
              '<div class="plot-title"><span>' + esc(spec.title) + '</span>' +
              '<span class="val" data-val="' + i + '">--</span></div>' +
              plotSvg(spec, span) +
              '<div class="cursor" data-cursor="' + i + '"></div></div>';
    });
    el.signals.innerHTML = html || '<div class="missing">no signals available for this perspective</div>';

    specs.forEach(function (spec, i) {
      PLOTS.push({
        spec: spec,
        cursor: el.signals.querySelector('[data-cursor="' + i + '"]'),
        valueEl: el.signals.querySelector('[data-val="' + i + '"]')
      });
    });
    updateSignalCursors();
  }

  function plotSvg(spec, span) {
    var pts = spec.points || [];
    var W = 600, H = 58, pad = 4;
    if (pts.length < 2) return '<svg viewBox="0 0 ' + W + ' ' + H + '" preserveAspectRatio="none"></svg>';
    var lo, hi;
    if (spec.fixed) { lo = spec.fixed[0]; hi = spec.fixed[1]; }
    else {
      lo = Infinity; hi = -Infinity;
      pts.forEach(function (p) { var v = p[spec.field]; if (typeof v === 'number') { lo = Math.min(lo, v); hi = Math.max(hi, v); } });
      if (!isFinite(lo)) { lo = 0; hi = 1; }
      if (hi - lo < 1e-6) { hi = lo + 1; }
      var m = (hi - lo) * 0.08; lo -= m; hi += m;
    }
    function X(t) { return pad + (t - span[0]) / (span[1] - span[0]) * (W - 2 * pad); }
    function Y(v) { return H - pad - (v - lo) / (hi - lo) * (H - 2 * pad); }

    var d = '';
    pts.forEach(function (p, i) {
      var v = p[spec.field];
      if (typeof v !== 'number') return;
      d += (d ? 'L' : 'M') + X(p.t).toFixed(1) + ' ' + Y(v).toFixed(1) + ' ';
    });
    var zero = (lo < 0 && hi > 0)
      ? '<line x1="0" y1="' + Y(0).toFixed(1) + '" x2="' + W + '" y2="' + Y(0).toFixed(1) +
        '" stroke="' + cssVar('--line') + '" stroke-width="1" vector-effect="non-scaling-stroke"></line>' : '';
    return '<svg viewBox="0 0 ' + W + ' ' + H + '" preserveAspectRatio="none">' + zero +
           '<path d="' + d + '" fill="none" stroke="' + spec.color +
           '" stroke-width="1.5" vector-effect="non-scaling-stroke"></path>' +
           '<title>' + esc(spec.title) + ': ' + num(lo, 2) + ' .. ' + num(hi, 2) + '</title></svg>';
  }

  function updateSignalCursors() {
    var span = runSpan();
    var pct = (T - span[0]) / (span[1] - span[0]) * 100;
    PLOTS.forEach(function (plot) {
      if (plot.cursor) plot.cursor.style.left = pct.toFixed(3) + '%';
      var s = sampleAt(plot.spec.points, T);
      if (plot.valueEl) {
        plot.valueEl.textContent = s && typeof s[plot.spec.field] === 'number'
          ? num(s[plot.spec.field], 2) : 'no sample';
      }
    });
  }

  // ----------------------------------------------------------------- events

  function renderEvents() {
    var evs = (VIEW.events || []).slice().sort(function (a, b) { return a.t_peak - b.t_peak; });
    if (!evs.length) {
      el.events.innerHTML = '<div class="missing">no events for this perspective in this run</div>';
      return;
    }
    var html = '';
    evs.forEach(function (e, i) {
      var who = e.owners && e.owners.length > 1 ? e.owners.join('+') : e.participant_id;
      html += '<div class="event-row' + (OUTCOME_TYPES[e.event_type] ? ' outcome' : '') +
              '" data-ev="' + i + '" data-t="' + e.t_peak + '" data-node="' + esc(e.event_id) + '">' +
              '<span class="t">' + num(e.t_peak, 2) + ' s</span>' +
              '<span><span class="ty">' + esc(e.event_type) + '</span> ' +
              '<span class="meta">' + esc(who) + (e.subject ? ' / ' + esc(e.subject) : '') +
              (valueSummary(e.values) ? ' -- ' + esc(valueSummary(e.values)) : '') + '</span></span>' +
              '<span class="meta">c ' + num(e.confidence, 2) + '</span></div>';
    });
    el.events.innerHTML = html;
    el.events.onclick = function (ev) {
      var row = ev.target.closest('.event-row');
      if (!row) return;
      seek(parseFloat(row.getAttribute('data-t')));
      selectNode(row.getAttribute('data-node'));
    };
    updateEventHighlight();
  }

  function updateEventHighlight() {
    Array.prototype.forEach.call(el.events.querySelectorAll('.event-row'), function (row) {
      var t = parseFloat(row.getAttribute('data-t'));
      row.classList.toggle('active', Math.abs(t - T) <= 0.3);
    });
  }

  // ------------------------------------------------------------ causal DAG

  var GRAPH_INDEX = null;   // {byId, out, inn, nodes, edges}

  /* SVG DAG laid out with time on the x axis and one lane per participant
   * (per event family when a single participant owns the whole graph). Time on
   * an axis is the point: a causal claim that runs backwards in time is then
   * visible as a backwards arrow rather than hidden in a spring layout. */
  function renderGraph() {
    var graph = VIEW.causal;
    SELECTED = null;
    HIGHLIGHT = { nodes: {}, edges: {} };
    el['graph-detail'].textContent = 'No node selected.';
    if (!graph || !graph.nodes || !graph.nodes.length) {
      el.graph.innerHTML = '<div class="missing">' + esc(VIEW.missingCausal) +
        ' -- not available for this run.</div>';
      GRAPH_INDEX = null;
      return;
    }

    var nodes = graph.nodes.slice().sort(function (a, b) { return a.t_peak - b.t_peak; });
    var edges = graph.edges || [];
    GRAPH_INDEX = indexGraph(nodes, edges);

    var lanesByKey = {}, laneOrder = [];
    var multiParticipant = uniqueCount(nodes, function (n) { return n.participant_id; }) > 1;
    nodes.forEach(function (n) {
      var key = multiParticipant ? n.participant_id : eventFamily(n.event_type);
      if (!(key in lanesByKey)) { lanesByKey[key] = { key: key, rows: [], nodes: [] }; laneOrder.push(key); }
      lanesByKey[key].nodes.push(n);
    });
    laneOrder.sort();

    var t0 = nodes[0].t_peak, t1 = nodes[nodes.length - 1].t_peak;
    if (t1 - t0 < 1e-6) t1 = t0 + 1;
    var NW = 132, NH = 20, ROW = 26, PADL = 96, PADR = 40, PADT = 16, AXIS = 30;
    var W = Math.max(860, Math.round((t1 - t0) * 120) + PADL + PADR);
    function X(t) { return PADL + (t - t0) / (t1 - t0) * (W - PADL - PADR - NW); }

    var y = PADT, pos = {}, laneBands = [];
    laneOrder.forEach(function (key) {
      var lane = lanesByKey[key];
      var rows = [];
      lane.nodes.forEach(function (n) {
        var x = X(n.t_peak);
        var r = 0;
        while (r < rows.length && rows[r] > x - 6) r++;   // 6 px gutter
        if (r === rows.length) rows.push(0);
        rows[r] = x + NW;
        pos[n.event_id] = { x: x, y: y + r * ROW, w: NW, h: NH, node: n };
      });
      laneBands.push({ key: key, y0: y - 6, h: Math.max(1, rows.length) * ROW + 6 });
      y += Math.max(1, rows.length) * ROW + 12;
    });
    var H = y + AXIS;

    var svg = '<svg width="' + W + '" height="' + H + '" viewBox="0 0 ' + W + ' ' + H + '">';
    svg += '<defs><marker id="arrow" markerWidth="7" markerHeight="7" refX="6.5" refY="2.5" orient="auto">' +
           '<path d="M0,0 L6,2.5 L0,5 z" fill="' + cssVar('--muted') + '"></path></marker></defs>';

    laneBands.forEach(function (band) {
      svg += '<text x="6" y="' + (band.y0 + 16) + '" fill="' + cssVar('--muted') +
             '" font-size="11">' + esc(band.key) + '</text>';
      svg += '<line x1="' + (PADL - 8) + '" y1="' + band.y0 + '" x2="' + (W - 8) + '" y2="' + band.y0 +
             '" stroke="' + cssVar('--line') + '" stroke-width="1"></line>';
    });

    edges.forEach(function (e, i) {
      var a = pos[e.source], b = pos[e.target];
      if (!a || !b) return;
      var x1 = a.x + a.w, y1 = a.y + a.h / 2, x2 = b.x, y2 = b.y + b.h / 2;
      var mx = (x1 + x2) / 2;
      var op = (0.12 + 0.88 * clamp(e.confidence, 0, 1)).toFixed(3);
      svg += '<path class="gedge" data-edge="' + i + '" d="M' + x1.toFixed(1) + ' ' + y1.toFixed(1) +
             ' C' + mx.toFixed(1) + ' ' + y1.toFixed(1) + ' ' + mx.toFixed(1) + ' ' + y2.toFixed(1) +
             ' ' + x2.toFixed(1) + ' ' + y2.toFixed(1) + '" fill="none" stroke="' + cssVar('--muted') +
             '" stroke-opacity="' + op + '" stroke-width="1.4" marker-end="url(#arrow)">' +
             '<title>' + esc(e.edge_type + '  conf ' + num(e.confidence, 2) +
             (e.rule ? '  rule ' + e.rule : '')) + '</title></path>';
    });

    nodes.forEach(function (n) {
      var p = pos[n.event_id];
      var fill = provenanceColor(n.provenance);
      svg += '<g class="gnode" data-node="' + esc(n.event_id) + '">' +
             '<rect x="' + p.x.toFixed(1) + '" y="' + p.y.toFixed(1) + '" width="' + p.w + '" height="' + p.h +
             '" rx="3" fill="' + fill + '" fill-opacity="' + (0.35 + 0.6 * clamp(n.confidence, 0, 1)).toFixed(2) +
             '" stroke="' + participantColor(n.participant_id) + '"></rect>' +
             '<rect x="' + p.x.toFixed(1) + '" y="' + p.y.toFixed(1) + '" width="4" height="' + p.h +
             '" fill="' + participantColor(n.participant_id) + '"></rect>' +
             '<text x="' + (p.x + 8).toFixed(1) + '" y="' + (p.y + 14).toFixed(1) + '">' +
             esc(shorten(n.event_type, 19)) + '</text>' +
             '<title>' + esc(n.event_type + '  ' + num(n.t_peak, 2) + ' s  ' + n.participant_id +
             (n.subject ? ' / ' + n.subject : '') + '  conf ' + num(n.confidence, 2)) + '</title></g>';
    });

    // Time axis, so a reader can price the horizontal distance between causes.
    svg += '<line x1="' + PADL + '" y1="' + (H - AXIS + 8) + '" x2="' + (W - PADR) + '" y2="' + (H - AXIS + 8) +
           '" stroke="' + cssVar('--line') + '"></line>';
    var ticks = 6;
    for (var k = 0; k <= ticks; k++) {
      var tv = t0 + (t1 - t0) * k / ticks;
      var xv = X(tv) + 0;
      svg += '<line x1="' + xv.toFixed(1) + '" y1="' + (H - AXIS + 8) + '" x2="' + xv.toFixed(1) + '" y2="' + (H - AXIS + 13) +
             '" stroke="' + cssVar('--line') + '"></line>' +
             '<text x="' + xv.toFixed(1) + '" y="' + (H - AXIS + 25) + '" fill="' + cssVar('--muted') +
             '" font-size="10">' + num(tv, 1) + ' s</text>';
    }
    svg += '</svg>';
    el.graph.innerHTML = svg;

    el.graph.onclick = function (ev) {
      var g = ev.target.closest('.gnode');
      if (g) selectNode(g.getAttribute('data-node'));
    };
  }

  function indexGraph(nodes, edges) {
    var byId = {}, out = {}, inn = {};
    nodes.forEach(function (n) { byId[n.event_id] = n; out[n.event_id] = []; inn[n.event_id] = []; });
    edges.forEach(function (e, i) {
      if (out[e.source]) out[e.source].push(i);
      if (inn[e.target]) inn[e.target].push(i);
    });
    return { byId: byId, out: out, inn: inn, nodes: nodes, edges: edges };
  }

  function uniqueCount(items, key) {
    var seen = {};
    items.forEach(function (it) { seen[key(it)] = 1; });
    return Object.keys(seen).length;
  }

  function eventFamily(type) {
    if (OUTCOME_TYPES[type]) return 'outcome';
    if (/^(RADAR|RANGE|RAPID|LOW_TTC|CRITICAL_TTC|LATERAL|CUT_IN|PREDICTED|CONFLICT|TARGET)/.test(type)) return 'interaction';
    return 'own behaviour';
  }

  function shorten(s, n) { return s.length <= n ? s : s.slice(0, n - 1) + '…'; }

  /* Selecting a node highlights the causal path between it and the outcome.
   *
   * For a non-outcome node that means: every node and edge that lies on some
   * directed path from it to an outcome event. It is computed as the
   * intersection of forward reachability from the node with backward
   * reachability from the outcomes -- linear, and it cannot blow up the way
   * enumerating simple paths would on a dense graph.
   * For an outcome node itself the interesting question is the reverse, so the
   * highlight becomes everything that can reach it. */
  function selectNode(nodeId) {
    if (!GRAPH_INDEX || !GRAPH_INDEX.byId[nodeId]) return;
    SELECTED = nodeId;
    var node = GRAPH_INDEX.byId[nodeId];
    var outcomes = GRAPH_INDEX.nodes.filter(function (n) { return OUTCOME_TYPES[n.event_type]; })
                                    .map(function (n) { return n.event_id; });
    var nodeSet = {}, edgeSet = {}, pathNote;

    if (OUTCOME_TYPES[node.event_type]) {
      var back = reach(nodeId, 'inn');
      nodeSet = back.nodes; edgeSet = back.edges;
      pathNote = 'everything that can reach this outcome (' +
                 (Object.keys(nodeSet).length - 1) + ' upstream nodes)';
    } else {
      var fwd = reach(nodeId, 'out');
      var backFromOutcomes = { nodes: {}, edges: {} };
      outcomes.forEach(function (oid) {
        var r = reach(oid, 'inn');
        Object.keys(r.nodes).forEach(function (k) { backFromOutcomes.nodes[k] = 1; });
        Object.keys(r.edges).forEach(function (k) { backFromOutcomes.edges[k] = 1; });
      });
      Object.keys(fwd.nodes).forEach(function (k) { if (backFromOutcomes.nodes[k]) nodeSet[k] = 1; });
      Object.keys(fwd.edges).forEach(function (k) {
        var e = GRAPH_INDEX.edges[k];
        if (nodeSet[e.source] && nodeSet[e.target]) edgeSet[k] = 1;
      });
      nodeSet[nodeId] = 1;
      pathNote = Object.keys(nodeSet).length > 1
        ? 'on a causal path to an outcome through ' + (Object.keys(nodeSet).length - 1) + ' node(s)'
        : 'NO causal path from this node reaches an outcome event in this graph';
    }

    HIGHLIGHT = { nodes: nodeSet, edges: edgeSet };
    applyHighlight();
    showNodeDetail(node, pathNote);
    seek(node.t_peak);
  }

  function reach(startId, dir) {
    var nodes = {}, edges = {}, stack = [startId];
    nodes[startId] = 1;
    while (stack.length) {
      var cur = stack.pop();
      (GRAPH_INDEX[dir][cur] || []).forEach(function (ei) {
        var e = GRAPH_INDEX.edges[ei];
        var next = dir === 'out' ? e.target : e.source;
        edges[ei] = 1;
        if (!nodes[next]) { nodes[next] = 1; stack.push(next); }
      });
    }
    return { nodes: nodes, edges: edges };
  }

  function applyHighlight() {
    var any = Object.keys(HIGHLIGHT.nodes).length > 0;
    Array.prototype.forEach.call(el.graph.querySelectorAll('.gnode'), function (g) {
      var id = g.getAttribute('data-node');
      g.classList.toggle('hl', id === SELECTED);
      g.classList.toggle('dim', any && !HIGHLIGHT.nodes[id]);
    });
    Array.prototype.forEach.call(el.graph.querySelectorAll('.gedge'), function (p) {
      var i = p.getAttribute('data-edge');
      p.classList.toggle('hl', !!HIGHLIGHT.edges[i]);
      p.classList.toggle('dim', any && !HIGHLIGHT.edges[i]);
    });
  }

  function showNodeDetail(n, pathNote) {
    var rows = [
      ['event', n.event_type],
      ['id', n.event_id],
      ['time', num(n.t_start, 2) + ' .. ' + num(n.t_peak, 2) + ' .. ' + num(n.t_end, 2) + ' s'],
      ['observer', (n.owners && n.owners.length ? n.owners.join(', ') : n.participant_id)],
      ['subject', n.subject || '(self)'],
      ['confidence', num(n.confidence, 3)],
      ['provenance', n.provenance],
      ['values', valueSummary(n.values) || '(none)'],
      ['evidence', (n.evidence_refs || []).join(', ') || '(none)'],
      ['path', pathNote]
    ];
    el['graph-detail'].innerHTML = '<strong>' + esc(n.event_type) + '</strong><dl>' +
      rows.map(function (r) { return '<dt>' + esc(r[0]) + '</dt><dd>' + esc(r[1]) + '</dd>'; }).join('') +
      '</dl>';
  }

  // --------------------------------------------------------------- checking

  function renderChecking() {
    var block = DATA.checking;
    if (!block || !block.results || !block.results.length) {
      el.checking.innerHTML = '<div class="missing">model-checking results are not available for this run.' +
        noteHint('checking') + '</div>';
      return;
    }
    // A local view shows its own verdicts; fused/oracle views show all of them,
    // labelled by participant, because neither owns a trace of its own.
    var rows = block.results.filter(function (r) {
      return VIEW.kind !== 'local' || r.participant_id === VIEW.id;
    });
    if (!rows.length) {
      el.checking.innerHTML = '<div class="missing">no property verdicts for ' + esc(VIEW.id) + '.</div>';
      return;
    }
    var byRef = {};
    (block.counterexamples || []).forEach(function (c) { byRef[c.counterexample_ref] = c; });

    var html = '<table class="grid"><thead><tr><th>property</th><th>vehicle</th><th>verdict</th>' +
               '<th>counterexample</th><th>why</th></tr></thead><tbody>';
    rows.forEach(function (r) {
      var iv = (r.violating_intervals || [])[0];
      var cex = r.counterexample_ref ? byRef[r.counterexample_ref] : null;
      var target = iv ? iv[0] : null;
      html += '<tr' + (target !== null ? ' class="clickable" data-seek="' + target + '"' : '') + '>' +
              '<td class="mono">' + esc(r.property_id) + '</td>' +
              '<td>' + esc(r.participant_id) + '</td>' +
              '<td><span class="chip ' + esc(r.status) + '">' + esc(r.status) + '</span></td>' +
              '<td class="num">' + (iv ? num(iv[0], 2) + ' .. ' + num(iv[1], 2) + ' s' +
                (cex ? ' (' + cex.n_samples + ' samples)' : '') : '--') + '</td>' +
              '<td>' + esc(r.reason || '') + '</td></tr>';
    });
    html += '</tbody></table>';
    if (block.summary) {
      html += '<div class="meta" style="margin-top:6px;color:var(--muted);font-size:12px">run totals: ' +
              esc(JSON.stringify(block.summary)) + '</div>';
    }
    el.checking.innerHTML = html;
    el.checking.onclick = function (ev) {
      var tr = ev.target.closest('tr.clickable');
      if (tr) seek(parseFloat(tr.getAttribute('data-seek')));
    };
  }

  // --------------------------------------------------------------- identity

  /* Who was that? The answer differs per layer, and the panel says which layer
   * is answering -- a local view never borrows the fusion layer's hypothesis. */
  function renderIdentity() {
    if (VIEW.kind === 'local') {
      var p = DATA.participants[VIEW.id];
      var ids = Object.keys(p.tracks || {}).sort();
      if (!ids.length) {
        el.identity.innerHTML = '<div class="missing">vehicle ' + esc(VIEW.id) +
          ' held no radar track in this run, so it can identify nobody from its own evidence.</div>';
        return;
      }
      var html = '<table class="grid"><thead><tr><th>track</th><th class="num">first</th>' +
                 '<th class="num">last</th><th class="num">samples</th><th class="num">mean conf</th>' +
                 '<th>identity</th></tr></thead><tbody>';
      ids.forEach(function (tid) {
        var pts = p.tracks[tid];
        var mean = pts.reduce(function (a, r) { return a + (r.confidence || 0); }, 0) / pts.length;
        html += '<tr class="clickable" data-seek="' + pts[0].t + '"><td class="mono">' + esc(tid) + '</td>' +
                '<td class="num">' + num(pts[0].t, 2) + '</td><td class="num">' + num(pts[pts.length - 1].t, 2) + '</td>' +
                '<td class="num">' + pts.length + '</td><td class="num">' + num(mean, 2) + '</td>' +
                '<td><em>unknown to this vehicle</em></td></tr>';
      });
      html += '</tbody></table><p class="missing">Onboard radar yields an anonymous track id. ' +
              'Mapping a track onto another participant is a fusion-layer inference and is shown only in the FUSED view.</p>';
      el.identity.innerHTML = html;
      el.identity.onclick = function (ev) {
        var tr = ev.target.closest('tr.clickable');
        if (tr) seek(parseFloat(tr.getAttribute('data-seek')));
      };
      return;
    }

    if (VIEW.kind === 'fused') {
      var assoc = (DATA.fusion && DATA.fusion.association) || [];
      if (!assoc.length) {
        el.identity.innerHTML = '<div class="missing">no track association was recorded for this run.' +
          noteHint('fusion') + '</div>';
        return;
      }
      var out = '<table class="grid"><thead><tr><th>claim</th><th>status</th><th class="num">rmse</th>' +
                '<th class="num">overlap</th><th>reason</th></tr></thead><tbody>';
      assoc.forEach(function (a) {
        out += '<tr><td class="mono">' + esc(identityClaim(a)) + '</td>' +
               '<td><span class="chip ' + esc(a.status) + '">' + esc(a.status) + '</span></td>' +
               '<td class="num">' + num(a.rmse_m, 2) + ' m</td>' +
               '<td class="num">' + num(a.overlap_s, 2) + ' s</td>' +
               '<td>' + esc(a.reason || '') +
               (a.runner_up ? ' | runner-up ' + esc(a.runner_up) + ' margin ' + num(a.runner_up_margin, 2) : '') +
               '</td></tr>';
      });
      out += '</tbody></table>';
      el.identity.innerHTML = out;
      return;
    }

    var pairs = (DATA.oracle.summary && DATA.oracle.summary.collision_pairs) || [];
    el.identity.innerHTML = pairs.length
      ? '<p>Ground truth needs no association. Recorded collision pairs:</p><ul>' +
        pairs.map(function (c) {
          return '<li class="mono">' + esc(c.a) + ' / ' + esc(c.b) + ' at ' + num(c.t, 2) + ' s</li>';
        }).join('') + '</ul>'
      : '<div class="missing">no collision pair recorded in the ground truth.</div>';
  }

  /* Required rendering of an uncertain identity, e.g.
   *   "track A::T003 -> B? 0.41 AMBIGUOUS". */
  function identityClaim(a) {
    var target = a.assigned_participant ||
      (a.candidates && a.candidates.length ? a.candidates[0].participant_id : null);
    if (!target) return 'track ' + a.track_id + ' -> ? (no candidate) ' + a.status;
    var mark = a.status === 'RESOLVED' ? '' : '?';
    return 'track ' + a.track_id + ' -> ' + target + mark + ' ' + num(a.confidence, 2) + ' ' + a.status;
  }

  // ------------------------------------------------------------ attribution

  /* The final answer, and the one place where saying nothing is the correct
   * output: without a counterfactual artifact the viewer must not name anybody.
   */
  function renderAttribution() {
    var cf = DATA.counterfactual;
    var contribution = cf && cf.contribution;
    var rows = contribution ? contributionRows(contribution) : [];

    if (!rows.length) {
      el.attribution.innerHTML =
        '<div class="insufficient">INSUFFICIENT EVIDENCE' +
        '<div class="why">' +
        (contribution
          ? 'A counterfactual analysis exists for this run but attributes no contribution that the evidence supports.'
          : 'No counterfactual replay has been run for this run directory, so no causal contribution can be attributed to any participant.') +
        noteHint('counterfactual') + '</div></div>';
      return;
    }

    var max = rows.reduce(function (m, r) { return Math.max(m, Math.abs(r.score)); }, 0) || 1;
    var html = '<table class="grid"><thead><tr><th>factor</th><th class="num">contribution</th>' +
               '<th style="width:40%">share</th><th>detail</th></tr></thead><tbody>';
    rows.forEach(function (r) {
      html += '<tr><td class="mono">' + esc(r.label) + '</td>' +
              '<td class="num">' + num(r.score, 3) + '</td>' +
              '<td><span class="bar" style="width:' + (Math.abs(r.score) / max * 100).toFixed(1) + '%"></span></td>' +
              '<td class="meta">' + esc(r.detail || '') + '</td></tr>';
    });
    html += '</tbody></table>' +
      '<p class="missing">Contributions come from counterfactual replays of this scenario; they rank ' +
      'interventions by their measured effect on the outcome, not people by blame.</p>';
    el.attribution.innerHTML = html;
  }

  /* The counterfactual artifact is produced by a separate stage, so read it
   * defensively: take the first recognised container of rows and require a
   * numeric score. An unreadable shape yields no rows, which the caller turns
   * into INSUFFICIENT EVIDENCE rather than a guess. */
  function contributionRows(contribution) {
    if (contribution.status === 'INSUFFICIENT_EVIDENCE' || contribution.insufficient_evidence === true) return [];
    var containers = ['contributions', 'ranking', 'rows', 'per_participant', 'participants', 'factors'];
    for (var i = 0; i < containers.length; i++) {
      var c = contribution[containers[i]];
      if (!c) continue;
      var rows = [];
      if (Array.isArray(c)) {
        c.forEach(function (item) {
          if (!item || typeof item !== 'object') return;
          var score = firstNumber(item, ['contribution', 'score', 'value', 'weight', 'necessity', 'impact']);
          var label = firstString(item, ['label', 'factor', 'event_id', 'intervention_id', 'action_id', 'participant_id']);
          if (score !== null && label !== null) rows.push({ label: label, score: score, detail: item.reason || item.detail || '' });
        });
      } else if (typeof c === 'object') {
        Object.keys(c).sort().forEach(function (k) {
          var v = c[k];
          if (typeof v === 'number') rows.push({ label: k, score: v, detail: '' });
          else if (v && typeof v === 'object') {
            var score = firstNumber(v, ['contribution', 'score', 'value', 'weight', 'necessity', 'impact']);
            if (score !== null) rows.push({ label: k, score: score, detail: v.reason || v.detail || '' });
          }
        });
      }
      if (rows.length) return rows.sort(function (a, b) { return Math.abs(b.score) - Math.abs(a.score); });
    }
    return [];
  }

  function firstNumber(obj, keys) {
    for (var i = 0; i < keys.length; i++) {
      if (typeof obj[keys[i]] === 'number' && isFinite(obj[keys[i]])) return obj[keys[i]];
    }
    return null;
  }

  function firstString(obj, keys) {
    for (var i = 0; i < keys.length; i++) {
      if (typeof obj[keys[i]] === 'string' && obj[keys[i]]) return obj[keys[i]];
    }
    return null;
  }

  // ------------------------------------------------------------------ notes

  function noteHint(block) {
    var notes = (DATA.notes || []).filter(function (n) { return n.block === block || n.block.indexOf(block + '.') === 0; });
    if (!notes.length) return '';
    return ' <span class="mono">(' + esc(notes[0].message) + ')</span>';
  }

  function renderNotes() {
    var notes = (DATA.notes || []).slice();
    ['fusion', 'checking', 'counterfactual', 'evaluation'].forEach(function (k) {
      if (DATA[k] && DATA[k].notes) notes = notes.concat(DATA[k].notes);
    });
    if (DATA.oracle && DATA.oracle.notes) notes = notes.concat(DATA.oracle.notes);
    Object.keys(DATA.participants || {}).forEach(function (pid) {
      notes = notes.concat(DATA.participants[pid].notes || []);
    });
    var sampling = DATA.sampling || {};
    var decimated = [];
    Object.keys(DATA.participants || {}).forEach(function (pid) {
      var s = (DATA.participants[pid].sampling || {});
      ['telemetry', 'controls'].forEach(function (k) {
        if (s[k] && s[k].decimated) decimated.push(pid + '.' + k + ' 1:' + s[k].stride);
      });
    });
    el.notes.innerHTML =
      '<div>bundle schema ' + esc(DATA.schema_version) + ' | max ' + esc(sampling.max_samples) +
      ' samples per series' + (decimated.length ? ' | decimated: ' + esc(decimated.join(', ')) : ' | no series decimated') + '</div>' +
      (notes.length
        ? '<ul>' + notes.map(function (n) {
            return '<li><span class="mono">' + esc(n.block) + '</span>: ' + esc(n.message) +
                   (n.paths && n.paths.length ? ' <span class="mono">[' + esc(n.paths.join(', ')) + ']</span>' : '') + '</li>';
          }).join('') + '</ul>'
        : '<div>every expected artifact was present.</div>');
  }

  document.addEventListener('DOMContentLoaded', boot);
})();

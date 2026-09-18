/*
  The incident viewer.

  One rule governs this file: it renders what the artifacts say and computes
  nothing it could get wrong. Where a number appears on screen it was read from
  run_data.json, not derived here -- a viewer that re-derived a metric could
  disagree with the run it is displaying, and then a reader would have no way to
  tell which was right.

  The second rule is that absence is shown, never filled in. A run with no
  camera, no merged timeline or no responsibility layer says so in the place the
  content would have been. A blank panel looks identical whether nothing was
  found or nothing was run, and those are very different things.
*/

'use strict';

const OUTCOME_TYPES = new Set(['COLLISION', 'NEAR_MISS', 'POST_IMPACT_STOP']);
const NON_ACTION_TYPES = new Set([
  'NO_STOP_AFTER_STOP_SIGN', 'NO_BRAKING_RESPONSE', 'NO_YIELD_RESPONSE',
  'NO_EVASIVE_RESPONSE', 'CONFLICT_ENTRY_WITHOUT_DECELERATION',
  'CONTINUED_ACCELERATION_DURING_CONFLICT',
]);
const ROAD_TYPES = new Set([
  'STOP_SIGN_DETECTED', 'YIELD_SIGN_DETECTED', 'STOP_LINE_DETECTED',
  'STOP_LINE_CROSSED', 'LANE_MARKING_CROSSED', 'SOLID_LINE_CROSSED',
  'ROAD_BOUNDARY_CROSSED',
]);

// Exactly the string the bundle stamps on its oracle block. Kept identical on
// purpose: if the two ever drift, a reader could be shown privileged content
// under a warning that no longer matches what the artifact claims.
const PRIVILEGED_WARNING = 'PRIVILEGED GROUND TRUTH - EVALUATION ONLY';

// What a reader is looking at, said in the place they are looking. A viewer that
// showed a local graph and a merged graph in the same frame, unlabelled, would
// invite exactly the confusion this project exists to avoid: one vehicle's
// account is not the incident.
const PERSPECTIVES = {
  local: {
    badge: 'LOCAL RECONSTRUCTION',
    note: 'one vehicle, its own sensors, its own clock.',
  },
  fused: {
    badge: 'FUSED RECONSTRUCTION',
    note: 'the merged account, built only from what the vehicles recorded.',
  },
  truth: {
    badge: PRIVILEGED_WARNING,
    note: 'read from exact simulator state. Never available to inference.',
  },
};

const state = {
  bundle: null,
  vehicle: null,
  camera: null,
  graphMode: 'inferred',
};

// --- small helpers --------------------------------------------------------

const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => Array.from(document.querySelectorAll(sel));

function el(tag, attrs, ...children) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v === null || v === undefined) continue;
    if (k === 'class') node.className = v;
    else if (k === 'text') node.textContent = v;
    else if (k.startsWith('on')) node.addEventListener(k.slice(2), v);
    else node.setAttribute(k, v);
  }
  for (const child of children.flat()) {
    if (child === null || child === undefined) continue;
    node.append(child.nodeType ? child : document.createTextNode(String(child)));
  }
  return node;
}

function svgEl(tag, attrs) {
  const node = document.createElementNS('http://www.w3.org/2000/svg', tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v !== null && v !== undefined) node.setAttribute(k, String(v));
  }
  return node;
}

function secs(v) {
  return v === null || v === undefined ? '—' : Number(v).toFixed(2);
}

function rowClass(eventType) {
  if (OUTCOME_TYPES.has(eventType)) return 'outcome';
  if (NON_ACTION_TYPES.has(eventType)) return 'nonaction';
  if (ROAD_TYPES.has(eventType)) return 'road';
  return '';
}

function valueText(row) {
  const values = row.values || {};
  const parts = Object.entries(values).map(([k, v]) => `${k}=${Number(v).toFixed(2)}`);
  return parts.join('  ');
}

function badge(kind) {
  const spec = PERSPECTIVES[kind];
  return el('div', { class: `perspective ${kind}` },
    el('span', { class: 'badge', text: spec.badge }),
    el('span', { class: 'note', text: spec.note }));
}

function notice(host, title, body) {
  host.hidden = false;
  host.replaceChildren(el('strong', { text: title }), document.createTextNode(body));
}

// --- masthead -------------------------------------------------------------

function renderMasthead() {
  const run = state.bundle.run || {};
  $('#scenario-title').textContent =
    `${run.scenario_id || 'run'} — ${(run.variant || '').replace(/_/g, ' ')}`;
  $('#scenario-description').textContent = run.description || '';

  const outcome = run.outcome || 'unknown';
  const outcomeEl = $('#fact-outcome');
  outcomeEl.textContent = String(outcome).replace(/_/g, ' ');
  outcomeEl.className = `fact-value ${outcome}`;

  $('#fact-vehicles').textContent = (run.participant_ids || []).join(', ') || '—';

  const globalLog = ((state.bundle.logs || {}).global) || null;
  $('#fact-clock').textContent = globalLog
    ? describeClock(globalLog)
    : 'not merged';

  $('#footer-run').textContent = run.run_dir || '';
}

function describeClock(globalLog) {
  if (!globalLog.common_time_available) {
    const n = (globalLog.unaligned_participants || []).length;
    return n ? `${n} recorder(s) unaligned` : 'no common time';
  }
  const method = globalLog.clock_method || '';
  if (method === 'acquisition_start_marker') return 'aligned by harness marker';
  return 'aligned by shared contact';
}

// --- reconstruction -------------------------------------------------------

function renderReconstruction() {
  const logs = state.bundle.logs || {};
  const locals = logs.local || {};
  const ids = Object.keys(locals).sort();

  const host = $('#vehicle-switch');
  host.replaceChildren(...ids.map((pid) =>
    el('button', {
      class: `chip${pid === state.vehicle ? ' on' : ''}`,
      text: `Vehicle ${pid}`,
      onclick: () => { state.vehicle = pid; renderReconstruction(); },
    })
  ));
  if (!ids.length) {
    host.replaceChildren(el('span', { class: 'untested', text: 'no local logs in this run' }));
  }
  if (state.vehicle === null && ids.length) state.vehicle = ids[0];

  $('#local-badge').replaceChildren(badge('local'));
  $('#global-badge').replaceChildren(badge('fused'));
  renderLocalLog(locals[state.vehicle]);
  renderGlobalLog(logs.global);
}

function renderLocalLog(log) {
  const body = $('#local-log tbody');
  if (!log) {
    body.replaceChildren(el('tr', {}, el('td', { colspan: '6', class: 'untested',
      text: 'no local log for this vehicle' })));
    return;
  }
  body.replaceChildren(...(log.rows || []).map((row) =>
    el('tr', {
      class: `${rowClass(row.event_type)} seekable`,
      onclick: () => seekVideo(row.participant, row.t_local),
    },
      el('td', { class: 't', text: secs(row.t_local) }),
      el('td', { class: 'event', text: row.event_type }),
      el('td', { text: row.subject || '' }),
      el('td', { class: 'evidence', text: row.source_sensor || '' }),
      el('td', { class: 'value', text: valueText(row) }),
      el('td', { class: 'num', text: Number(row.confidence).toFixed(2) })
    )
  ));
}

function renderGlobalLog(log) {
  const explain = $('#global-log-explain');
  const wrap = $('#global-log-wrap');
  const missing = $('#global-log-missing');
  const body = $('#global-log tbody');
  missing.hidden = true;

  if (!log) {
    wrap.hidden = true;
    explain.textContent = '';
    notice(missing, 'No merged log.',
      'Fusion has not been run for this run, so only the separate local ' +
      'timelines above are available.');
    return;
  }

  wrap.hidden = false;
  if (log.common_time_available) {
    explain.textContent =
      'Every row on one axis. ' + (log.clock_caveat || log.note || '');
  } else {
    const unaligned = (log.unaligned_participants || []).join(', ');
    explain.textContent = '';
    notice(missing, 'No shared collision or contact anchor.',
      `Rows for ${unaligned || 'some recorders'} keep only their own clock and ` +
      'are shown with a dash in the common-time column. Simulator time is not ' +
      'substituted, so this run has no single merged timeline.');
  }

  body.replaceChildren(...(log.rows || []).map((row) => {
    const aligned = row.t_common !== null && row.t_common !== undefined;
    return el('tr', { class: rowClass(row.event_type) },
      el('td', { class: aligned ? 't' : 't unaligned',
        text: aligned ? secs(row.t_common) : `— (${secs(row.t_local)} local)` }),
      el('td', {}, el('span', { class: `who who-${row.participant}`, text: row.participant })),
      el('td', { class: 'event', text: row.event_type }),
      el('td', { text: row.subject || '' }),
      el('td', { class: 'evidence', text: row.source_sensor || '' })
    );
  }));
}

// --- graph ----------------------------------------------------------------

function graphFor(mode) {
  const fusion = state.bundle.fusion || {};
  const oracle = state.bundle.oracle || {};
  if (mode === 'truth') return oracle.observable_causal_graph || null;
  return fusion.causal_graph || null;
}

function renderGraph() {
  $$('[data-graph]').forEach((b) =>
    b.classList.toggle('on', b.dataset.graph === state.graphMode));

  const canvas = $('#graph-canvas');
  const missing = $('#graph-missing');
  const counts = $('#graph-counts');
  const legend = $('#graph-legend');
  missing.hidden = true;
  legend.hidden = state.graphMode !== 'diff';

  if (state.graphMode === 'diff') {
    // A diff draws the privileged graph coloured by what the reconstruction
    // found, so it is privileged content too and is badged as such.
    $('#graph-badge').replaceChildren(badge('truth'));
    renderDiff(canvas, missing, counts);
    return;
  }

  $('#graph-badge').replaceChildren(
    badge(state.graphMode === 'truth' ? 'truth' : 'fused')
  );

  const graph = graphFor(state.graphMode);
  if (!graph || !(graph.nodes || []).length) {
    canvas.replaceChildren();
    counts.textContent = '';
    notice(missing,
      state.graphMode === 'truth' ? 'No observable ground truth.' : 'No reconstructed graph.',
      state.graphMode === 'truth'
        ? 'This run has no observable ground-truth graph, so there is nothing ' +
          'comparable to show. The scenario design reference is not shown here ' +
          'because it asserts scripted actions no reconstruction can emit.'
        : 'Fusion has not produced a causal graph for this run.');
    return;
  }

  drawGraph(canvas, graph.nodes, graph.edges || [], null);
  counts.textContent =
    `${graph.nodes.length} events, ${(graph.edges || []).length} causal edges.`;
}

function renderDiff(canvas, missing, counts) {
  const diff = (state.bundle.evaluation || {}).graph_diff;
  const account = diff && diff.accounts
    ? (diff.accounts.global_inferred || diff.accounts.simple_fusion)
    : null;
  const truth = graphFor('truth');

  if (!account || !truth) {
    canvas.replaceChildren();
    counts.textContent = '';
    notice(missing, 'No comparison available.',
      'The difference view needs both an observable ground truth and a scored ' +
      'comparison against it; one of them is missing for this run.');
    return;
  }

  // Status per reference node, straight from the comparison rows. The viewer
  // does not decide what matched -- the evaluation already did, and disagreeing
  // with it here would be worse than showing nothing.
  const status = new Map();
  for (const row of account.node_rows || []) {
    if (row.reference_id) status.set(row.reference_id, row.status);
  }
  // 'extra' is what the comparison calls a node the reconstruction asserted and
  // the reference does not have. Getting this string wrong would silently report
  // zero false positives, which is the most flattering possible mistake.
  const extras = (account.node_rows || []).filter((r) => r.status === 'extra');

  drawGraph(canvas, truth.nodes, truth.edges || [], status);

  const nodes = account.nodes || {};
  counts.textContent =
    `recovered ${nodes.n_matched || 0} of ${nodes.n_reference || 0} ground-truth ` +
    `events (recall ${Number(nodes.recall || 0).toFixed(3)}), ` +
    `invented ${extras.length}; ` +
    `edge F1 ${Number((account.edges || {}).f1 || 0).toFixed(3)}.`;
}

function drawGraph(canvas, nodes, edges, status) {
  const bands = Array.from(new Set(nodes.map((n) => n.participant_id))).sort();
  const times = nodes.map((n) => n.t_peak);
  const t0 = Math.min(...times);
  const t1 = Math.max(...times);
  const span = Math.max(t1 - t0, 0.001);

  const padL = 64, padR = 40, padT = 26, bandH = 96;
  const width = Math.max(900, nodes.length * 34);
  const height = padT + bands.length * bandH + 34;

  const svg = svgEl('svg', { width, height, viewBox: `0 0 ${width} ${height}` });
  const x = (t) => padL + ((t - t0) / span) * (width - padL - padR);

  // Bands, one per vehicle, so a reader can see whose events these are without
  // reading a single label.
  bands.forEach((pid, i) => {
    const y = padT + i * bandH;
    svg.append(svgEl('line', {
      x1: padL, y1: y + bandH / 2, x2: width - padR, y2: y + bandH / 2,
      class: 'axis-line',
    }));
    const label = svgEl('text', { x: 10, y: y + bandH / 2 + 4, class: 'band-label' });
    label.textContent = pid;
    svg.append(label);
  });

  // A few time ticks. Enough to orient, not enough to clutter.
  for (let i = 0; i <= 4; i += 1) {
    const t = t0 + (span * i) / 4;
    const tick = svgEl('text', { x: x(t), y: height - 10, class: 'axis-tick' });
    tick.textContent = `${t.toFixed(1)}s`;
    svg.append(tick);
  }

  const place = new Map();
  const perBand = new Map();
  for (const node of nodes.slice().sort((a, b) => a.t_peak - b.t_peak)) {
    const bandIndex = bands.indexOf(node.participant_id);
    const key = `${bandIndex}`;
    const slot = (perBand.get(key) || 0);
    perBand.set(key, (slot + 1) % 3);
    const cx = x(node.t_peak);
    const cy = padT + bandIndex * bandH + bandH / 2 + (slot - 1) * 24;
    place.set(node.event_id, { cx, cy });
  }

  for (const edge of edges) {
    const a = place.get(edge.source);
    const b = place.get(edge.target);
    if (!a || !b) continue;
    let cls = 'edge';
    if (status) {
      const ok = status.get(edge.source) === 'matched' && status.get(edge.target) === 'matched';
      cls += ok ? ' matched' : ' missing';
    }
    const midX = (a.cx + b.cx) / 2;
    svg.append(svgEl('path', {
      d: `M ${a.cx} ${a.cy} C ${midX} ${a.cy}, ${midX} ${b.cy}, ${b.cx} ${b.cy}`,
      class: cls,
    }));
  }

  for (const node of nodes) {
    const at = place.get(node.event_id);
    if (!at) continue;
    const isOutcome = OUTCOME_TYPES.has(node.event_type);
    let fill = '#8b93a1';
    if (status) {
      const s = status.get(node.event_id);
      fill = s === 'matched' ? '#1f7a4d' : '#b03a2e';
    } else if (isOutcome) {
      fill = '#b03a2e';
    } else {
      fill = ['#1f5f9e', '#9e5b1f', '#4a1f9e'][bands.indexOf(node.participant_id) % 3];
    }
    svg.append(svgEl('circle', {
      cx: at.cx, cy: at.cy, r: isOutcome ? 6 : 4, fill,
    }));
    const label = svgEl('text', {
      x: at.cx + 7, y: at.cy + 3, class: 'node-label',
    });
    label.textContent = shortType(node.event_type);
    const title = svgEl('title');
    title.textContent =
      `${node.event_type}  ${node.participant_id}` +
      `${node.subject ? ' → ' + node.subject : ''}  t=${secs(node.t_peak)}`;
    label.append(title);
    svg.append(label);
  }

  canvas.replaceChildren(svg);
}

function shortType(type) {
  // Full type names overlap into an unreadable smear at this density. The tooltip
  // carries the full name, so nothing is lost.
  return String(type)
    .replace('SIGNIFICANT_', '')
    .replace('_LIKE_MANEUVER', '')
    .replace('CONFLICT_REGION_', 'CONFLICT_')
    .replace('CONTINUED_ACCELERATION_DURING_CONFLICT', 'KEPT_ACCELERATING')
    .replace('CONFLICT_ENTRY_WITHOUT_DECELERATION', 'ENTERED_UNSLOWED');
}

// --- responsibility -------------------------------------------------------

function renderResponsibility() {
  const block = state.bundle.responsibility || null;
  const cards = $('#responsibility-cards');
  const priority = $('#priority-card');
  const missing = $('#responsibility-missing');
  missing.hidden = true;

  if (!block || !block.report) {
    cards.replaceChildren();
    priority.replaceChildren();
    notice(missing, 'No responsibility findings.',
      'The normative layer has not run for this run.');
  } else {
    const report = block.report;
    renderProtocolWarning();
    renderPriority(priority, report.priority || {});
    cards.replaceChildren(...Object.entries(report.findings || {})
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([pid, finding]) => renderFinding(pid, finding)));
  }

  renderFormal();
}

function renderProtocolWarning() {
  /*
    The but-for column below comes from counterfactual replays, and a replay run
    in a shared simulator session is not comparable with the factual run it is
    being compared against -- the server drifts. The verdict itself gives a
    reader no way to tell, so the protocol travels with it and this banner says
    when it was degraded.

    Three states, not two. A report written before the check existed carries no
    protocol block at all, and reading that as "it was fine" is exactly the
    mistake the record was added to prevent, so it gets its own message.
  */
  const host = $('#protocol-warning');
  const contribution = (state.bundle.counterfactual || {}).contribution || null;
  const protocol = contribution ? contribution.replay_protocol : null;
  host.hidden = true;

  if (!contribution) return;
  if (!protocol) {
    notice(host, 'Replay protocol not recorded.',
      'This attribution predates the protocol record, so whether each replay ' +
      'ran against a fresh simulator cannot be established from the artifact. ' +
      'That is not the same as it having been fine.');
    return;
  }
  if (protocol.effective !== 'fresh_server_per_replay') {
    notice(host, 'Degraded replay protocol.',
      (protocol.warning || '') + ' The but-for findings below rest on replays ' +
      'that shared a simulator session with each other, so they are not ' +
      'comparable with the factual run in the way a but-for claim requires.');
    return;
  }
  if (protocol.restarts_verified_fresh !== true) {
    notice(host, 'Fresh protocol configured but not verified.',
      'Each replay was configured to restart the simulator, but the restarts ' +
      'were not verified to have produced a fresh engine. A restart that ' +
      'silently reconnected to an orphaned server looks identical here.');
  }
}


function renderPriority(host, priority) {
  if (!priority.verdict) { host.replaceChildren(); return; }
  host.replaceChildren(
    el('div', { class: 'verdict', text:
      `Right of way: ${priority.verdict.replace(/_/g, ' ').toLowerCase()}` +
      (priority.has_priority ? ` — ${priority.has_priority}` : '') }),
    el('div', { class: 'why', text: priority.reason || '' })
  );
}

function renderFinding(pid, f) {
  const butFor = f.but_for_contribution || {};
  const verdictSpan = (value) => {
    const cls = value === 'yes' ? 'yes' : value === 'no' ? 'no' : 'untested';
    return el('span', { class: cls, text: value });
  };

  const dl = el('dl', {},
    el('dt', { text: 'Physical contributor' }),
    el('dd', {}, verdictSpan(f.physical_causal_contributor)),
    el('dt', { text: 'But-for' }),
    el('dd', {}, verdictSpan(butFor.verdict || 'not tested')),
    el('dt', { text: 'Rules broken' }),
    el('dd', { text: (f.traffic_control_violations || []).length
      ? f.traffic_control_violations.map((v) => v.node_type.replace(/_/g, ' ').toLowerCase()).join(', ')
      : 'none observed' }),
    el('dt', { text: 'Properties failed' }),
    el('dd', { text: (f.temporal_property_failures || []).length
      ? f.temporal_property_failures.map((p) => p.property_id).join(', ')
      : 'none' }),
    el('dt', { text: 'Non-actions' }),
    el('dd', { text: (f.non_action_evidence || []).length
      ? f.non_action_evidence.map((n) => n.event_type.replace(/_/g, ' ').toLowerCase()).join(', ')
      : 'none' }),
    el('dt', { text: 'Mitigating' }),
    el('dd', { text: (f.mitigating_actions || []).length
      ? `${f.mitigating_actions.length} response(s) to a threat it faced`
      : 'none' }),
    el('dt', { text: 'Prevention' }),
    el('dd', { text: (f.prevention_opportunities || []).length
      ? `${f.prevention_opportunities.length} opportunity(ies)`
      : 'none tested' })
  );

  return el('div', { class: 'card' },
    el('h3', { text: `Vehicle ${pid}` }),
    el('span', { class: `level ${f.responsibility_evidence}`,
      text: f.responsibility_evidence === 'insufficient'
        ? 'INSUFFICIENT EVIDENCE' : f.responsibility_evidence.toUpperCase() }),
    dl,
    el('div', { class: 'why', text: f.why || '' })
  );
}

function renderFormal() {
  const host = $('#formal-list');
  const missing = $('#formal-missing');
  missing.hidden = true;

  const formal = state.bundle.formal || null;
  if (!formal || !formal.results) {
    host.replaceChildren();
    notice(missing, 'No property results.', 'The property checker has not run for this run.');
    return;
  }

  host.replaceChildren(...(formal.results.results || []).map((r) => {
    const verdict = r.vacuous ? 'vacuous' : r.status;
    return el('div', { class: 'property' },
      el('div', { class: 'head' },
        el('span', { class: `verdict ${verdict}`, text: verdict }),
        el('strong', { text: r.property_id }),
        el('span', { text: r.title })
      ),
      el('div', { class: 'formula', text: r.formula || '' }),
      el('div', { class: 'reason', text: r.reason || '' })
    );
  }));
}

// --- video ----------------------------------------------------------------

function renderVideo() {
  const block = state.bundle.video || null;
  const missing = $('#video-missing');
  const stage = $('#video-stage');
  const switcher = $('#camera-switch');
  const timeline = $('#video-timeline');
  missing.hidden = true;

  if (!block || !block.per_participant) {
    switcher.replaceChildren();
    stage.hidden = true;
    // The timeline is an empty bordered strip when there is nothing to put in
    // it, which reads as a control that failed rather than as an absent one.
    timeline.hidden = true;
    timeline.replaceChildren();
    notice(missing, 'No camera recording.',
      'This run was recorded without a camera, which is a supported ' +
      'configuration — the V1 scenarios have no camera at all.');
    return;
  }

  stage.hidden = false;
  timeline.hidden = false;
  const ids = Object.keys(block.per_participant).sort();
  if (state.camera === null && ids.length) state.camera = ids[0];

  switcher.replaceChildren(...ids.map((pid) =>
    el('button', {
      class: `chip${pid === state.camera ? ' on' : ''}`,
      text: `Camera ${pid}`,
      onclick: () => { state.camera = pid; renderVideo(); },
    })
  ));

  const entry = block.per_participant[state.camera] || {};
  const player = $('#video-player');
  if (entry.available && entry.video_path) {
    player.src = `../${entry.video_path}`;
    player.hidden = false;
  } else {
    player.removeAttribute('src');
    player.hidden = true;
    notice(missing, 'Frames buffered but not encoded.',
      `Vehicle ${state.camera} has a frame index but no playable clip.`);
  }
  renderMarkers(timeline, entry.frame_index || {});
}

function renderMarkers(host, index) {
  const log = ((state.bundle.logs || {}).local || {})[state.camera];
  host.replaceChildren();
  if (!log || index.t_first === null || index.t_first === undefined) return;

  const t0 = index.t_first;
  const t1 = index.t_last;
  const span = Math.max(t1 - t0, 0.001);

  for (const row of log.rows || []) {
    if (row.t_local < t0 || row.t_local > t1) continue;
    const kind = rowClass(row.event_type) || 'event';
    if (!['outcome', 'nonaction', 'road'].includes(kind)) continue;
    const marker = el('div', {
      class: 'marker',
      'data-kind': kind,
      title: `${row.event_type} at ${secs(row.t_local)}s`,
      onclick: () => seekVideo(state.camera, row.t_local),
    }, el('span', { class: 'tip', text: shortType(row.event_type) }));
    marker.style.left = `${((row.t_local - t0) / span) * 100}%`;
    host.append(marker);
  }
}

function seekVideo(participant, tLocal) {
  const block = state.bundle.video || null;
  if (!block || !block.per_participant || !block.per_participant[participant]) return;
  state.camera = participant;
  showTab('video');
  renderVideo();
  const player = $('#video-player');
  const index = block.per_participant[participant].frame_index || {};
  if (index.t_first === null || index.t_first === undefined) return;
  // The clip starts at the recorder's t_first, so a seek offset is the event
  // time minus that -- the video element knows nothing about vehicle clocks.
  player.currentTime = Math.max(0, tLocal - index.t_first);
}

// --- tabs, notes, boot ----------------------------------------------------

function showTab(name) {
  $$('.tab').forEach((b) => b.setAttribute('aria-selected', String(b.dataset.tab === name)));
  $$('.panel').forEach((p) => { p.hidden = p.id !== `panel-${name}`; });
}

function renderNotes() {
  const host = $('#notes');
  const notes = state.bundle.notes || [];
  host.replaceChildren(...notes.map((n) =>
    el('li', { text: `${n.block}: ${n.reason || n.message || ''}` })));
  if (!notes.length) host.replaceChildren(el('li', { text: 'nothing missing.' }));
}

async function boot() {
  let bundle;
  try {
    const response = await fetch('run_data.json');
    bundle = await response.json();
  } catch (err) {
    document.body.replaceChildren(el('div', { class: 'notice' },
      el('strong', { text: 'Could not load run_data.json.' }),
      'Serve this directory over HTTP (scripts/serve_viewer.py) rather than ' +
      'opening the file directly — browsers block local fetches.'));
    return;
  }
  state.bundle = bundle;

  renderMasthead();
  renderReconstruction();
  renderGraph();
  renderResponsibility();
  renderVideo();
  renderNotes();

  $$('.tab').forEach((b) => b.addEventListener('click', () => showTab(b.dataset.tab)));
  $$('[data-graph]').forEach((b) => b.addEventListener('click', () => {
    state.graphMode = b.dataset.graph;
    renderGraph();
  }));
  $('#toggle-notes').addEventListener('click', () => {
    const notes = $('#notes');
    notes.hidden = !notes.hidden;
  });
  showTab('reconstruction');
}

boot();

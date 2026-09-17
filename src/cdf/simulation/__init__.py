"""CARLA-facing scenario generation.

This is the only subpackage that imports ``carla``. It is *test-generation*
code: scenario controllers legitimately know the scripted world because they
create it. Nothing here may be imported by ``cdf.local`` or ``cdf.fusion``.
"""

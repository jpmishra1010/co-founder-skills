# Installation and execution are different

The public installation route is the independently maintained `npx skills add` CLI.
The installed main skill already contains all 12 internal workflows. A separate
Co-founder npm publication is unnecessary. Optional wrapper skills require the main
skill alongside them; do not assume the installer automatically adds dependencies.

Installation copies instructions and resources. Python 3.10+ is still needed for
project_context.py, cf.py, quality_gate.py and other bundled Python helpers. If the
runtime is unavailable, explain the missing dependency and stop before claiming
project/asset integrity or verification was executed. Do not bypass required project
binding or silently install dependencies. Request authorization for needed setup.

Do not invoke the old Python installer's update/uninstall actions on a skills-CLI
installation. They have different ownership markers, paths and link behavior. Never
read credentials or call a model API to resolve an installation problem.

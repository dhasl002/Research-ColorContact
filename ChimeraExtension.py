# --- UCSF Chimera Copyright ---
# Copyright (c) 2000 Regents of the University of California.
# All rights reserved.  This software provided pursuant to a
# license agreement containing restrictions on its disclosure,
# duplication and use.  This notice must be embedded in or
# attached to all copies, including partial copies, of the
# software or any revisions or derivations thereof.
# --- UCSF Chimera Copyright ---

import chimera.extension

class ModelPanelEMO(chimera.extension.EMO):
	def name(self):
		return 'ColorContacts'
	def description(self):
		return 'allows color coded contacts to be visible'
	def categories(self):
		return ['Utilities']
	def activate(self):
		from chimera.dialogs import display
		display(self.module('base').ModelPanel.name)
		return None

chimera.extension.manager.registerExtension(ModelPanelEMO(__file__))

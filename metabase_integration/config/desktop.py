# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		# {
		# 	"module_name": "Metabase Integration",
		# 	"color": "grey",
		# 	"icon": "octicon octicon-file-directory",
		# 	"type": "module",
		# 	"label": _("Metabase Integration")
		# },
		{
			'module_name': 'Metabase Integration',
			'category': 'Places',
			'label': _('Metabase Dashboard'),
			'icon': 'octicon octicon-graph',
			'type': 'link',
			'link': '#metabase-dashboard',
			'color': '#FF4136',
			'standard': 1,
			'idx': 11
		},
	]

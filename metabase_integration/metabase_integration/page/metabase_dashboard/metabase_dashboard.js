/* eslint require-jsdoc: 0 */

frappe.pages['metabase-dashboard'].on_page_load = (wrapper) => {
	// init page
	const page = frappe.ui.make_app_page({
		'parent': wrapper,
		'title': 'Dashboard',
		'single_column': true,
	});

	new MetabaseDashboard(page, wrapper);
};

class MetabaseDashboard {
	constructor(page, wrapper) {
		this.currentDashboard = false;
		this.wrapper = wrapper;
		this.pageMain = $(page.main);
		this.pageAction = (
			$(this.wrapper)
				.find('div.page-head div.page-actions')
		);
		this.pageTitle = $(this.wrapper).find('div.title-text');

		this.init();
	}

	init() {
		this.createSelectionField();
	}

	showIframe() {
		this.getSettings().then(
			(r) => {
				// set variable
				this.settings = r.message;
				this.resizer = this.settings.resizer;
				this.iframeUrl = this.settings.iframeUrl;
				this.name = this.settings.name;

				if (this.iframeUrl && this.resizer) {
					// prepare html
					const iFrameHtml = `
						<script id="resizer" src="${this.resizer}"></script>
						<iframe
							src="${this.iframeUrl}"
							frameborder="0"
							width=100%
							onload="iFrameResize({}, this)"
							allowtransparency
						></iframe>
					`;

					// append html to page
					this.iFrame = $(iFrameHtml).appendTo(this.pageMain);
				}
			}
		);
	}

	getSettings() {
		return frappe.call({
			'method': 'metabase_integration.metabase_integration.doctype.metabase_dashboard.get_url',
			'args': {
				'dashboard': this.dashboardName,
			},
		});
	}

	createSelectionField() {
		// create dashboard selection field
		this.selectionField = frappe.ui.form.make_control({
			'parent': this.pageAction,
			'df': {
				'fieldname': 'Dashboard',
				'fieldtype': 'Link',
				'options': 'Metabase Dashboard',
				'onchange': () => {
					const dashboardName = this.selectionField.get_value();
					if (dashboardName) {
						this.dashboardName = dashboardName;
						if (this.currentDashboard != this.dashboardName) {
							// clear page html
							this.pageMain.empty();

							this.showIframe();
							this.changeTitle();

							// set current dashboard
							this.currentDashboard = this.dashboardName;
						}
						// clear input
						this.selectionField.set_input('');
					}
				},
				'get_query': () => {
					return {
						'filters': {
							'is_active': 1,
						},
					};
				},
				'placeholder': 'Select Dashboard',
			},
			'render_input': true,
		});

		// change css
		this.pageAction.removeClass('page-actions');
		this.selectionField.$wrapper.css('text-align', 'left');
	}

	changeTitle() {
		this.pageTitle.text(`${this.dashboardName} Dashboard`);
	}
}

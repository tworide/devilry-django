/**
 * List of groups.
 */
Ext.define('devilry_subjectadmin.view.managestudents.ListOfGroups' ,{
    extend: 'devilry_subjectadmin.view.managestudents.GridOfGroupsBase',
    alias: 'widget.listofgroups',
    cls: 'devilry_subjectadmin_listofgroups',
    store: 'Groups',
    hideHeaders: true,

    getColumns: function() {
        return [this.getGroupInfoColConfig(), this.getMetadataColConfig()];
    },

    initComponent: function() {
        Ext.apply(this, {
            dockedItems: [{
                xtype: 'toolbar',
                dock: 'top',
                items: [{
                    xtype: 'combobox',
                    itemId: 'sortby',
                    queryMode: 'local',
                    valueField: 'value',
                    displayField: 'label',
                    forceSelection: true,
                    editable: false,
                    value: 'fullname', // NOTE: This must match the argument to _sortBy in _onRenderListOfGroups in the controller
                    flex: 1,
                    store: Ext.create('Ext.data.Store', {
                        fields: ['value', 'label'],
                        data : [
                            {value:'fullname', label:"Sort by: Full name"},
                            {value:'lastname', label:"Sort by: Last name"},
                            {value:'username', label:"Sort by: Username"}
                        ]
                    })
                }, {
                    xtype: 'combobox',
                    itemId: 'viewselect',
                    queryMode: 'local',
                    valueField: 'value',
                    displayField: 'label',
                    forceSelection: true,
                    editable: false,
                    value: 'flat',
                    flex: 1,
                    matchFieldWidth: false,
                    store: Ext.create('Ext.data.Store', {
                        fields: ['value', 'label'],
                        data : [
                            {value:'flat', label:"View: Flat"},
                            {value:'examiner', label:"View: Group by examiner"},
                            {value:'is_passing_grade', label:"View: Group by passed/failed"},
                            {value:'is_open', label:"View: Group by open/closed"},
                        ]
                    })
                }]
            }, {
                xtype: 'toolbar',
                ui: 'footer',
                dock: 'bottom',
                defaults: {
                    scale: 'medium',
                },
                items: [{
                    xtype: 'button',
                    itemId: 'selectButton',
                    text: gettext('Select'),
                    menu: this._createSelectMenu({
                        itemId: 'replaceSelectionMenu',
                        title: gettext('Replace current selection'),
                        prefixItems: [{
                            itemId: 'selectall',
                            text: gettext('Select all')
                        }, {
                            itemId: 'deselectall',
                            text: gettext('Deselect all')
                        }, {
                            itemId: 'invertselection',
                            text: gettext('Invert selection')
                        }, '-']
                    })
                }, {
                    xtype: 'button',
                    itemId: 'addToSelectionButton',
                    text: gettext('Add to selection'),
                    menu: this._createSelectMenu({
                        title: gettext('Add to current selection'),
                        itemId: 'addToSelectionMenu'
                    })
                }, '->', {
                    xtype: 'button',
                    itemId: 'addstudents',
                    iconCls: 'icon-add-24',
                    text: gettext('Add students')
                }]
            }],
        });
        this.callParent(arguments);
    },


    /**
     * @param {String} [config.title] Title of the menu
     * @param {[Object]} [config.prefixItems] Prefixed to the items in the menu, under the title.
     */
    _createSelectMenu: function(config) {
        var menuitems = [Ext.String.format('<b>{0}:</b>', config.title)];
        if(config.prefixItems) {
            Ext.Array.push(menuitems, config.prefixItems);
        }
        Ext.Array.push(menuitems, [{

        // Status
            text: pgettext('group', 'Status'),
            menu: [{
                itemId: 'selectStatusOpen',
                text: pgettext('group', 'Open')
            }, {
                itemId: 'selectStatusClosed',
                text: pgettext('group', 'Closed')
            }]

        // Grade
        }, {
            text: pgettext('group', 'Grade'),
            menu: [{
                itemId: 'selectGradePassed',
                text: pgettext('group', 'Passed')
            }, {
                itemId: 'selectGradeFailed',
                text: pgettext('group', 'Failed')
            }, '-', {
                text: 'TODO: Will list of all current grades here unless there are more than XXX (20?)'
            }]

        // Number of deliveries
        }, {
            text: gettext('Number of deliveries'),
            menu: [{
                itemId: 'selectHasDeliveries',
                text: gettext('Has deliveries')
            }, {
                itemId: 'selectNoDeliveries',
                text: gettext('No deliveries')
            }, '-', {
                text: 'TOOD: Will list all numbers of deliveries.'
            }]

        // With examiner
        }, {
            text: gettext('With examiner'),
            menu: [{
                itemId: 'selectHasExaminer',
                text: gettext('Has examiner(s)')
            }, {
                itemId: 'selectNoExaminer',
                text: gettext('No examiner(s)')
            }, {
                text: 'TODO: Will list all related examiners'
            }]
        }]);
        var menu = {
            xtype: 'menu',
            plain: true,
            itemId: config.itemId,
            items: menuitems
        }
        return menu;
    }
});

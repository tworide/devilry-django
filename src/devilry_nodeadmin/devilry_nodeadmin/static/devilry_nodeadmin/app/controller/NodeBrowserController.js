Ext.define('devilry_nodeadmin.controller.NodeBrowserController', {
    extend: 'Ext.app.Controller',

    views: [
        'NodeBrowserOverview'
    ],

    requires: [
        'devilry_nodeadmin.view.NodeChildrenList',
        'devilry_nodeadmin.view.NodeDetailsOverview',
        'devilry_nodeadmin.view.NodeParentLink'
    ],

    stores: [
        'NodeChildren',
        'NodeDetails'
    ],

    models: [
        'Details',
        'Node'
    ],

    refs: [{
        ref: 'overview',
        selector: 'nodebrowseroverview'
    }, {
        ref: 'primary',
        selector: 'nodebrowseroverview #primary'
    }, {
        ref: 'secondary',
        selector: 'nodebrowseroverview #secondary'
    }],

    init: function() {
        this.control({
            'viewport nodebrowseroverview #primary': {
                render: this._onRenderPrimary
            }
        })
    },

    _onRenderPrimary: function() {
        var node_pk = this.getOverview().node_pk;
        this.getPrimary().add([{
            xtype: 'nodeparentlink',
            node_pk: node_pk
        }, {
            xtype: 'nodechildrenlist',
            node_pk: node_pk
        }]);
        this.getSecondary().add([{
            xtype: 'nodedetailsoverview',
            node_pk: node_pk
        }]);
    }
});

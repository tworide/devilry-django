// Autogenerated by the dev_coreextjsmodels script. DO NOT CHANGE MANUALLY

/*******************************************************************************
 * NOTE: You will need to add the following before your application code:
 *
 *    Ext.Loader.setConfig({
 *        enabled: true,
 *        paths: {
 *            'devilry': DevilrySettings.DEVILRY_STATIC_URL + '/extjs_classes'
 *        }
 *    });
 *    Ext.syncRequire('devilry.extjshelpers.RestProxy');
 ******************************************************************************/
Ext.define('devilry.apps.examiner.simplified.SimplifiedDeadline', {
    extend: 'Ext.data.Model',
    requires: ['devilry.extjshelpers.RestProxy'],
    fields: [
        {
            "type": "int", 
            "name": "id"
        }, 
        {
            "type": "auto", 
            "name": "text"
        }, 
        {
            "type": "date", 
            "name": "deadline", 
            "dateFormat": "Y-m-d\\TH:i:s"
        }, 
        {
            "type": "auto", 
            "name": "assignment_group"
        }, 
        {
            "type": "auto", 
            "name": "number_of_deliveries"
        }, 
        {
            "type": "bool", 
            "name": "feedbacks_published"
        }, 
        {
            "type": "int", 
            "name": "assignment_group__parentnode__id"
        }, 
        {
            "type": "int", 
            "name": "assignment_group__parentnode__delivery_types"
        }, 
        {
            "type": "auto", 
            "name": "assignment_group__parentnode__short_name"
        }, 
        {
            "type": "auto", 
            "name": "assignment_group__parentnode__long_name"
        }, 
        {
            "type": "auto", 
            "name": "assignment_group__name"
        }, 
        {
            "type": "bool", 
            "name": "assignment_group__is_open"
        }, 
        {
            "type": "auto", 
            "name": "assignment_group__candidates__identifier"
        }, 
        {
            "type": "int", 
            "name": "assignment_group__parentnode__parentnode__id"
        }, 
        {
            "type": "auto", 
            "name": "assignment_group__parentnode__parentnode__short_name"
        }, 
        {
            "type": "auto", 
            "name": "assignment_group__parentnode__parentnode__long_name"
        }, 
        {
            "type": "int", 
            "name": "assignment_group__parentnode__parentnode__parentnode__id"
        }, 
        {
            "type": "auto", 
            "name": "assignment_group__parentnode__parentnode__parentnode__short_name"
        }, 
        {
            "type": "auto", 
            "name": "assignment_group__parentnode__parentnode__parentnode__long_name"
        }
    ],
    idProperty: 'id',
    proxy: {
        type: 'devilryrestproxy',
        url: '/examiner/restfulsimplifieddeadline/',
        headers: {
            'X_DEVILRY_USE_EXTJS': true
        },
        extraParams: {
            getdata_in_qrystring: true,
            result_fieldgroups: '["assignment", "assignment_group", "assignment_group_users", "period", "subject"]'
        },
        reader: {
            type: 'json',
            root: 'items',
            totalProperty: 'total'
        },
        writer: {
            type: 'json'
        }
    }
});
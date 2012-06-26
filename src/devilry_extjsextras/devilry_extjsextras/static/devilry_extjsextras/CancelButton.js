/**
Cancel button
*/ 
Ext.define('devilry_extjsextras.CancelButton', {
    extend: 'Ext.button.Button',
    alias: 'widget.cancelbutton',
    scale: 'medium',
    cls: 'devilry_cancelbutton',
    text: pgettext('uibutton', 'Cancel')
});

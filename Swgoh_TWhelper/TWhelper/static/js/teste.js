$(document).ready(function() {
    //`popup` / `inline`
    $.fn.editable.defaults.mode = 'inline';

    $('#stdid').editable();
    $('#stdname').editable();
    $('#stdemail').editable({type:'email'});

    $('#stdcourse').editable({
        type: 'select',
        title: 'Select Course',
        placement: 'right',
        value: 1,
		require:true,
        source: [
            {value: 1, text: 'M.C.A'},
            {value: 2, text: 'B.C.A'},
            {value: 3, text: 'P.G.D.C.A'},
            {value: 4, text: 'B.S.C IT'}
        ]
    });
});

$(document).ready(function () {
    var editor = ace.edit("editor");
    var editor_input = ace.edit("editor__input");

    function setEditor() {
        editor.setTheme("ace/theme/monokai");
        editor.session.setMode("ace/mode/javascript");
        editor.setOptions({
            autoScrollEditorIntoView: true,
            copyWithEmptySelection: true,
        });
// use setOptions method
        editor.setOption("mergeUndoDeltas", "always");
        editor.session.setMode("ace/mode/python");
        editor.session.setTabSize(4);
        editor.setHighlightActiveLine(true);
    };

    setEditor();

    const executeCodeBtn = document.querySelector('.editor__run');
    const resetCodeBtn = document.querySelector('.editor__reset');

    executeCodeBtn.addEventListener('click', () => {
        // Get input from the code editor
        var userCode = editor.getValue();

        console.log(userCode);
        console.log(typeof userCode);
        // Run the user code
        let formData = new FormData();
        formData.append('code', userCode);
        if (formData) {
            $.ajax({
                url: '{% url "calculate"%}',
                method: 'POST',
                data: formData,
                dataType: 'json',
                processData: false,
                contentType: false,
                success: function (data) {

                }

            });
        }
    });
});

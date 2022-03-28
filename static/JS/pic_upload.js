$(function() {
    $('#uploadButton').click(openDialog)
    $('#uploadPicture').change(updateImage);
})

function openDialog() {
    let pic = $( "#uploadPicture" );
    pic.click();
}

function updateImage() {
    $("#imageForm").submit();
}
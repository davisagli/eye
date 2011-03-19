jQuery(function($) {

var Eye = {};

Eye.update_info = function(nodepath) {
    $.ajax({
          url: nodepath,
          dataType: "json",
          success: function(data) {
            $('#info').html('<pre>' + data['info'] + '</pre>');
          }
     });
};

Eye.empty_info = function(){
    $("#info").text("");
};

Eye.build_tree = function(node) {
    if (node.data.title) { return ( Eye.build_tree(node.parent) + "/" + node.data.key); }
    else { return "" ; }
}; 

Eye.get_path = function(node) {
    var mypath = Eye.build_tree(node);
    return mypath;
};

$("#tree").dynatree({
    initAjax: {
        url: "/@@tree",
        data: { mode: "funnyMode" },
        dataType: "json"
        },
    onActivate: function(node) {
        Eye.update_info(Eye.get_path(node));
    },
    onDeactivate: function(node) {
        Eye.empty_info();
    },
    onLazyRead: function(node){
        node.appendAjax({
            url: Eye.get_path(node) + "/@@tree",
            data: {
                key: node.data.key,
                mode: "funnyMode"
            }
        });
    }
});

$('body').layout({
    east__size : 433,
    west__size : 433,
    north__size : 50,
    south__size : 450
});

});

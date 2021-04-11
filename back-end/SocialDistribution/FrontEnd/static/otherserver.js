discover_url = "https://nofun.herokuapp.com/";
var discover_token = "bc994a0507e90138def54fb44629df983d35fd4a";
outsideserver()
function outsideserver(){
  
    $.ajax({
        headers: {Authorization:'Token '+discover_token},
        type: 'GET',
        url: 'https://nofun.herokuapp.com/post-list/'
    })
    .done(function(data){
        console.log("server auth");
        console.log(data);
        var posts = data;
        if(posts.length != 0){
            for ( i = 0 ; i < posts.length; i++){
                var data = posts[i];
                console.log(data);
                //insert post data to DOM
                Fill_Discover_DOM(data,"showFollow","hideDel","hideEdit",1);
            }
        }
    });

}

function Fill_Discover_DOM(data,flag,deleteFlag,editFlag){
    persist_Discover_Likes(data.author.id,data.id,data,flag,deleteFlag,editFlag);
}

 //persist likes
function persist_Discover_Likes(author_id,post_id,data,flag,deleteFlag,editFlag){
    var author_id = author_id.split("https://nofun.herokuapp.com/author/")[1];
    var post_id = post_id.split("/");
    post_id = post_id[post_id.length - 1];
    console.log("THIS IS AUTHOR ID " + author_id);
    console.log("THIS IS POST ID " + post_id);
    $.ajax({
        headers: {Authorization:'Token '+discover_token},
        type: 'GET',
        url: discover_url+'author/'+author_id+'/posts/'+post_id +"/likes/"
    })
    .done(function(d){
        var like_c = d.length;
        var toggle_post_img;
        var toggle_post_text;
        console.log("Persist for foreign server");
        if(data.contentType == "image"){
            console.log("I AM AN IMAGE")
            toggle_post_img = "show_img_block";
            toggle_post_text =  "hide_post_text";
        }
        if(data.contentType == "text/image"){
            toggle_post_img = "show_img_block";
            toggle_post_text =  "hide_post_text";
        }
        if(data.contentType == "text/plain"){
            toggle_post_img = "hide_img_block";
            toggle_post_text = "show_post_text";
        }
    
        insert_discovery_Post("Follow",data,flag,deleteFlag,editFlag,like_c,toggle_post_img,toggle_post_text);
    });
}
function insert_discovery_Post(fs,data,flag,deleteFlag,editFlag,like_c,toggle_post_img,toggle_post_text){
    var followstats = fs;
    var pid_unclean = (data.id).split("/");
    var pid_clean = pid_unclean[pid_unclean.length - 1];
     console.log(pid_clean);
    const postHTML =  `<div class="posted-wrap">
        <div class="posted-w-h" >
            <div class="p-w-h-details">
                <div class="p-profile-wrap">
                    <div class="p-profile">
                    </div>
                </div>
                <div class="p-user-wrap">
                    <p>${data.author.displayName}</p>
                </div>
                <p class="follow-user ${data.author.id}" id="${flag}" onclick="followUser(this)">${followstats}</p>
            </div>
            <div class="del-post ${deleteFlag}"  id="${pid_clean}" onclick="deletePost(this)">
                <i class="material-icons" style="color:rgba(0,0,0,0.45)">delete_outline</i>
            </div>
            <div class="edit-post ${editFlag}">
                <i class="material-icons" style="color:rgba(0,0,0,0.45)">mode</i>
            </div>
        </div>
        <div class="p-title-wrap">
            <p>${data.title}</p>
        </div>
        <div class="post-text" id="${toggle_post_text}">
            <p>${data.content}</p>
        </div>
        <div class="posted-img-wrap" id="${toggle_post_img}">
            <img src="${data.content}" id="proimage">
        </div>
        <div class="like-count-w">
            <p id="like-count" class="${"like_row"+pid_clean}">${like_c + " likes"}</p><p id="${"comment-count_"+pid_clean}">${2} comments</p">
        </div>
        <div class="social-controls">

            <div class="like-w ${"thumb_"+data.author.id}" onclick="likepost(this)" id="${"thumb_"+pid_clean}">
                <div class="s-c-img">
                    <i class="material-icons">thumb_up</i>
                </div>
                <p>Like</p>
            </div>
            <div class="comment-w ${data.author.id}" onclick="toggle_discovery_Comments(this)" id="${pid_clean}">
                <div class="s-c-img">
                    <i class="material-icons">comment</i>
                </div>
                <p>Comment</p>
            </div>
            <div class="share-w">
                <div class="s-c-img">
                    <i class="material-icons">share</i>
                </div>
                <p>Share</p>
            </div>
        </div>
        <div class="o-comments" id="${"o-comment_"+pid_clean}">
            <div class="o-c-cell">
                <div class="oc-profile">

                </div>
                <div class="o-type-comment">
                    <input type="text" placeholder="Type your comments here" id="${"comment_input"+pid_clean}">
                </div>
                <div class="send-comment" onclick="addcomment(this)" id="${pid_clean}">
                    <i class="material-icons" style="color:white">send</i>
                </div>
            </div>
            <div class="o-r-cell" id="${"comment_cell"+pid_clean}">

            </div>
        </div>
    </div>`;
    $(".post-feed").append(postHTML);
}

var opened_discovery_comments = [];
function toggle_discovery_Comments(element){
    console.log(element)
    var commentblockid = "o-comment_"+element.id;
    if(!(opened_discovery_comments.includes(commentblockid))){
        opened_discovery_comments.push(commentblockid);
        document.getElementById(commentblockid).style.display = "inline-block";
        console.log("comment opened")
        console.log(opened_discovery_comments)
        fetch_discover_comment(element)
    }else{
        const index = opened_discovery_comments.indexOf(commentblockid);
        if (index > -1) {
            opened_discovery_comments.splice(index, 1);
        }
        console.log(opened_discovery_comments)
        document.getElementById(commentblockid).style.display = "none";
        $("#comment_cell"+element.id).empty();
        console.log("comment closed")
    }
}

function fetch_discover_comment(element){
    // var pid_unclean = (element.id).split("/");
    // var pid_clean = pid_unclean[pid_unclean.length - 1];
    //  console.log(pid_clean);

    var userid_unclean = element.className.split(" ");
    var userid_unclean2 = element.className.split("/");
    var userid_clean = userid_unclean2[userid_unclean2.length - 1];
    console.log(userid_clean);
    $.ajax({
        headers: {Authorization:'Token '+discover_token},
        type:"GET",
        url:discover_url+"author/"+userid_clean+"/posts/"+element.id+"/comments/"
    })
    .done(function(data){
        //MANIPULATE DOM
        console.log(data);
        for(i=0;i<data.length;i++){
            console.log(data[i].comment)
            var comment = data[i].comment;
            var c_cell = `<div class="o-r-details">
                <p>${comment}</p>
                <div class="c-p-wrap">
                    <div class="comment-profile"> <i class="material-icons" style="color:cornflowerblue">sentiment_satisfied_alt</i></div><p><span>${"Hard coded author name"}</span></p><div class="comment-time"><p>${data[i].published.split("T")[0]}</p><div/>
                </div>
            </div>`
            $("#comment_cell"+element.id).append(c_cell);
        }
    });
}
discover_url = "https://nofun.herokuapp.com/";
var discover_token = "1e2f83dc7c4e929464ae4e8d5c42f69b7983ceee";
outsideserver();
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
    $.ajax({
        headers: {Authorization:'Token '+discover_token},
        type: 'GET',
        url: discover_url+'author/'+author_id+'/posts/'+post_id +"/likes/"
    })
    .done(function(d){
        var like_c = d.length;
        var toggle_post_img;
        var toggle_post_text;
        if(data.contentType == "image"){
            console.log("I AM AN IMAGE")
            toggle_post_img = "show_img_block";
            toggle_post_text =  "hide_post_text";
        }
        else if(data.contentType == "text/image"){
            toggle_post_img = "show_img_block";
            toggle_post_text =  "hide_post_text";
        }
        else if(data.contentType == "text/plain"){
            toggle_post_img = "hide_img_block";
            toggle_post_text = "show_post_text";
        }
        else if(data.contentType == "text/markdown"){
            toggle_post_img = "hide_img_block";
            toggle_post_text = "show_post_text";
        }
        else{
            toggle_post_img = "hide_img_block";
            toggle_post_text = "show_post_text";
        }
        console.log("-------===--------");
        console.log(toggle_post_img);
        console.log(toggle_post_text);
        console.log("-------===--------");
        if(localStorage.getItem('uuid') != null){
            persistFollowStats_discover(localStorage.getItem('uuid'),data,flag,deleteFlag,editFlag,like_c,toggle_post_img,toggle_post_text);
        }else{
            insert_discovery_Post("Follow",data,flag,deleteFlag,editFlag,like_c,toggle_post_img,toggle_post_text);
        }
    
    });
}
function insert_discovery_Post(fs,data,flag,deleteFlag,editFlag,like_c,toggle_post_img,toggle_post_text){
    var followstats = fs;
    var pid_unclean = (data.id).split("/");
    var pid_clean = pid_unclean[pid_unclean.length - 1];
    var authorid_unclean = (data.author.id).split("/");
    var authorid_clean = authorid_unclean[authorid_unclean.length - 1];
    console.log(authorid_clean);
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
                <p class="follow-user ${"ftag_"+authorid_clean}" id="${flag}" onclick="follow_discover_User(this)">${followstats}</p>
            </div>
            <div class="del-post ${deleteFlag}"  id="${pid_clean}" onclick="deletePost(this)">
                <i class="material-icons" style="color:rgba(0,0,0,0.45)">delete_outline</i>
            </div>
            <div class="edit-post ${editFlag}">
                <i class="material-icons" style="color:rgba(0,0,0,0.45)">mode</i>
            </div>
        </div>
        <div class="p-title-wrap">
            <h3>${data.title}</h3>
        </div>
        <div class="post-text" id="${toggle_post_text}">
            <p>${data.content}</p>
        </div>
        <div class="posted-img-wrap" id="${toggle_post_img}">
            <img src="${data.content}" id="proimage">
        </div>
        <div class="like-count-w">
            <p id="like-count" class="${"like_row"+pid_clean}">${like_c + " likes"}</p><p id="${"comment-count_"+pid_clean}">${data.count} comments</p">
        </div>
        <div class="social-controls">

            <div class="like-w ${"thumb_"+authorid_clean}" onclick="likepost_discover(this)" id="${"thumb_"+pid_clean}">
                <div class="s-c-img">
                    <i class="material-icons">thumb_up</i>
                </div>
                <p>Like</p>
            </div>
            <div class="comment-w ${authorid_clean}" onclick="toggle_discovery_Comments(this)" id="${pid_clean}">
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
                <div class="send-comment ${authorid_clean}" onclick="addcomment_discover(this)" id="${pid_clean}">
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

function follow_discover_User(curTag){
    if (is_auth_user() == true){
        console.log("tapped follower tag")
        var arr = (curTag.className).split(' ');
        fid = arr[1];
        follow_discover_Request(fid,curTag)
    }else{
        //alert("sign in or sign up to send a friend request")
        document.getElementsByClassName('popup-auth')[0].style.display = "block";
    }
}

function follow_discover_Request(fid,curTag){
    console.log(curTag)
    data = {
        "actor":host_url + 'author/'+localStorage.getItem('uuid'),
        "object":discover_url+"author/"+fid 
    }
    $.ajax({
        headers: {Authorization:'Token '+discover_token},
        type:"POST",
        contentType: "application/json",
        data:JSON.stringify(data),
        url:discover_url+"friendrequest/"
    })
    .done(function(data){
        //MANIPULATE DOM
        console.log(data);
        curTag.innerHTML = "Request Sent";
        replaceall_discover(curTag);
    });
}

//replaces all follow request links of a particular user to "request sent"
function replaceall_discover(curtag){ 
    var cn = curtag.className.split(" ")[1];
    console.log("replace all is : "+cn)
    $('.'+cn).each(function(i, obj) {
        obj.innerHTML = "Request Sent";
    });
}

//persist follow status on each public post
function persistFollowStats_discover(fid,data,flag,deleteFlag,editFlag,like_c,toggle_post_img,toggle_post_text){
    var authorid_unclean = (data.author.id).split("/");
    var authorid_clean = authorid_unclean[authorid_unclean.length - 1];
    $.ajax({
        headers: {Authorization:'Token '+discover_token},
        type: 'GET',
        url: discover_url+ 'author/'+authorid_clean+'/followers/'+localStorage.getItem("uuid")
    })
    .done(function(dd){
        console.log("IN persistent follow stats");
        console.log(dd);
        var followstats;
        if(dd.status == "R"){
            followstats="Request Sent";
        }
        else if(dd.status == "A"){
            followstats="Friends";
        }
        else if(dd.status == "D"){
            followstats="Follow";
        }
        else{
            followstats="Follow";
        }
        insert_discovery_Post(followstats,data,flag,deleteFlag,editFlag,like_c,toggle_post_img,toggle_post_text);
        
    });
}




// //handling comments
function addcomment_discover(element){
    if (is_auth_user() == true){
        var authorid = element.className.split(" ")[1];
        var pid = element.id;
        console.log("pid is : "+pid)
        var textfield = document.getElementById("comment_input"+pid).value;
        if(textfield == ""){
            return
        }
        console.log(textfield)
        data = {
            "type":"comment",
            "author":localStorage.getItem('uuid'),
            "contentType":"contentType",
            "comment":textfield
        }
        $.ajax({
            type:"POST",
            headers: {Authorization:'Token '+discover_token},
            contentType: "application/json",
            data:JSON.stringify(data),
            url:discover_url+"author/"+authorid+"/posts/"+pid+"/comments/"
        })
        .done(function(data){
            //MANIPULATE DOM
            console.log(data);
            var res_comment_id = data.id.split("/");
            res_comment_id = res_comment_id[res_comment_id.length - 1];
            var c_cell = `
            <div class="o-r-details">
                <p><span>${displayName_cur}</span> ${textfield}</p>
                <div class="c-p-wrap">
                    <div class="comment-like-wrap ${authorid} ${res_comment_id} ${pid}" onclick="like_comment_discover(this)"><p>Like</p></div><div class="comment-profile"> <i class="material-icons" style="color:white;font-size:12px;">thumb_up</i></div><div class="comment-like-num"><p id="com-like_${res_comment_id}">0</p></div><div class="comment-tzone"><p>march 15th</p></div></div>
                </div>
            </div>`;
            $("#comment_cell"+pid).append(c_cell);
            var commentlabel = document.getElementById("comment-count_"+pid).innerHTML;
            var countvalarr = commentlabel.split(" ");
            var countval;
            countval = + countvalarr[0];
            countval+=1;
            console.log(commentlabel);
            document.getElementById("comment_input"+pid).value = ""
            document.getElementById("comment-count_"+pid).innerHTML = countval + "comments";
        });
    }else{
        //alert("sign in or sign up to comment on a post");
        document.getElementsByClassName('popup-auth')[0].style.display = "block";
    }
}

 //likepost
function likepost_discover(element){
    
    if (is_auth_user() == true){
        console.log("like_post func called")
        var authorid = element.className.split(" ")[1].slice(6);
        console.log("author id : "+authorid)
        var postid= (element.id).slice(6);
        //get author id
        var arr = (element.className).split(' ');
        var extract = arr[1];
        fid = extract.slice(6);
        data = {
            "author":localStorage.getItem('uuid')
        }
        $.ajax({
            type:"POST",
            headers: {Authorization:'Token '+discover_token},
            contentType: "application/json",
            data:JSON.stringify(data),
            url:discover_url+"author/"+authorid+"/posts/"+postid+"/likes/"
        })
        .done(function(data){
            //increment count
            var countvaljunk = document.getElementsByClassName("like_row"+postid)[0].innerHTML += 1;
            var countval = + countvaljunk.slice(0, -6)
            countval+=1;
            document.getElementsByClassName("like_row"+postid)[0].innerHTML = countval + " likes";
        })

    }else{
        //alert("sign in or sign up to like a post");
        document.getElementsByClassName('popup-auth')[0].style.display = "block";
    }

}

function fetch_discover_comment(element){
    var userid_unclean = element.className.split(" ");
    var userid_clean = userid_unclean[userid_unclean.length - 1];
    console.log("------")
    console.log(userid_clean)
    $.ajax({
        headers: {Authorization:'Token '+discover_token},
        type:"GET",
        url:discover_url+"author/"+userid_clean+"/posts/"+element.id+"/comments/"
    })
    .done(function(data){
        //MANIPULATE DOM
        console.log(data);
        getCommentlikes(data,element,userid_clean);
    });
}


async function getCommentlikes(data,element,userid_clean){
     for(i=0;i<data.length;i++){ 
        var clean_comment_id = data[i].id.split("/");
        console.log(data[i].id)
        clean_comment_id = clean_comment_id[clean_comment_id.length - 1];
        try{
            await $.ajax({
                headers: {Authorization:'Token '+discover_token},
                type: 'GET',
                url: discover_url+ 'author/'+userid_clean+'/posts/'+element.id+"/comments/"+clean_comment_id+"/likes/"
            })
            .done(function(commentarray){
                //get username of commenter 
                // GET  /author/<str:author_uuid>/
                fetchcommenter(commentarray,data,element,userid_clean,i,clean_comment_id)                
            });
        }catch{

        }     
     }
}

async function fetchcommenter(commentarray,data,element,userid_clean,i,clean_comment_id){
    var commenter_id = (data[i].author).split("/");
    var commenter_id = commenter_id[commenter_id.length - 1];
    //check where to get the user details from
    // if()

    try{
        await $.ajax({
            headers: {Authorization:'Token '+discover_token},
            type: 'GET',
            url: discover_url+ 'author/'+commenter_id+'/'
        })
        .done(function(commenterinfo){
            console.log(commenterinfo)
            // if(commenterinfo)
            console.log(commenterinfo)
            var commenter_dname = commenterinfo.displayName;
            var commentlikes = commentarray.length;
            var comment = data[i].comment;
            console.log(data[i].comment)
            var c_cell = `
            <div class="o-r-details">
                <p><span>${commenter_dname}</span> ${comment}</p>
                <div class="c-p-wrap">
                    <div class="comment-like-wrap ${userid_clean} ${clean_comment_id} ${element.id}" onclick="like_comment_discover(this)"><p>Like</p></div><div class="comment-profile"> <i class="material-icons" style="color:white;font-size:12px;">thumb_up</i></div><div class="comment-like-num"><p id="com-like_${clean_comment_id}">${commentlikes}</p></div><div class="comment-tzone"><p>${data[i].published.split("T")[0]}</p></div></div>
                </div>
            </div>`;
            $("#comment_cell"+element.id).append(c_cell);
        });
        
    }catch(error){
        console.log(error);
        //based on how group 20 handled their get request , we need to call another ajax in the error block to fetch from our server
        try{
            await $.ajax({
                type: 'GET',
                url: 'author/'+commenter_id+'/'
            })
            .done(function(localuserinfo){
                console.log("in local call");
                console.log(localuserinfo);
                var commenter_dname = localuserinfo.displayName;
                var commentlikes = commentarray.length;
                var comment = data[i].comment;
                console.log(data[i].comment)
                var c_cell = `
                <div class="o-r-details">
                    <p><span>${commenter_dname}</span> ${comment}</p>
                    <div class="c-p-wrap">
                        <div class="comment-like-wrap ${userid_clean} ${clean_comment_id} ${element.id}" onclick="like_comment_discover(this)"><p>Like</p></div><div class="comment-profile"> <i class="material-icons" style="color:white;font-size:12px;">thumb_up</i></div><div class="comment-like-num"><p id="com-like_${clean_comment_id}">${commentlikes}</p></div><div class="comment-tzone"><p>${data[i].published.split("T")[0]}</p></div></div>
                    </div>
                </div>`;
                $("#comment_cell"+element.id).append(c_cell);

            });
        }catch(err){
            console.log(err)
            console.log("in unknown(3rd group) group call");
            var commenter_dname = "unknown user";
            var commentlikes = commentarray.length;
            var comment = data[i].comment;
            console.log(data[i].comment)
            var c_cell = `
            <div class="o-r-details">
                <p><span>${commenter_dname}</span> ${comment}</p>
                <div class="c-p-wrap">
                    <div class="comment-like-wrap ${userid_clean} ${clean_comment_id} ${element.id}" onclick="like_comment_discover(this)"><p>Like</p></div><div class="comment-profile"><i class="material-icons" style="color:white;font-size:12px;">thumb_up</i></div><div class="comment-like-num"><p id="com-like_${clean_comment_id}">${commentlikes}</p></div><div class="comment-tzone"><p>${data[i].published.split("T")[0]}</p></div></div>
                </div>
            </div>`;
            $("#comment_cell"+element.id).append(c_cell);
        }
        
    }

}

//likepost
function like_comment_discover(element){
    
    if (is_auth_user() == true){
        console.log("like_post func called")
        var post_owner_id = element.className.split(" ")[1];
        var commentID = element.className.split(" ")[2];
        var postID = element.className.split(" ")[3];

        console.log("commenter id : "+post_owner_id);
        console.log("comment id : "+commentID);
        console.log("post id : "+postID);

        data = {
            "author":localStorage.getItem('uuid')
        }
        $.ajax({
            type:"POST",
            headers: {Authorization:'Token '+discover_token},
            contentType: "application/json",
            data:JSON.stringify(data),
            url:discover_url+"author/"+post_owner_id+"/posts/"+postID+"/comments/"+commentID+"/likes/"
        })
        .done(function(data){
            //increment count
            console.log(data);
            var countvaljunk = document.getElementById("com-like_"+commentID).innerHTML;
            var countval = + countvaljunk;
            countval+=1;
            document.getElementById("com-like_"+commentID).innerHTML = countval;
        })
    }else{
        //alert("sign in or sign up to like a post");
        document.getElementsByClassName('popup-auth')[0].style.display = "block";
    }
}

<template>
  <section>
  <div class="carte">
    <div class="topcarte"></div>
    <img id="profile" src="../../assets/profil.png" alt="" width="90" />
    <div class="bottomcarte">
      <h2>@John Doe</h2>
      <p id="email">test@gmail.com</p>
      <p id="citation">"Lorem ipsum dolor sit amet consectetur"</p>
    </div>
    <hr />
    <p style="height:2px"></p>
    <div class="lastPost" v-for="post in data" :key="post.id">
      <div class="post">
        <p id="post">{{ post.post }}</p>
        <div class="like">
          <p id="like">{{ post.like }}</p>
          <img
            src="../../assets/like.png"
            alt=""
            width="20"
            style="margin-top: -25px; opacity: 0.7"
          />
        </div>
      </div>
    </div>
    <hr />
    <div class="buttons">
      <div class="update">
        <img src="../../assets/update.png" alt="" width="17" />
        <p>Update profile</p>
      </div>
      <div class="addPost" data-toggle="modal" data-target="#addPost">
        <img src="../../assets/plus.png" alt="" width="17" />
        <p>Add new post</p>
      </div>
    </div>

    <!-- Modal -->
    <div class="modal fade" id="addPost" tabindex="-1" role="dialog" aria-labelledby="addPostCentertitre" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content" >
          <div class="modal-header">
            <h5 class="modal-titre" id="addPostLongtitre">Add new post</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <div class="postArea">
              <p style="font-size:13px; margin-bottom:0px">Your article here</p>
              <textarea id="tArea" rows="7"></textarea>
            </div>
            <div class="imageFac">
              <div id="app" class="container my-3">
                <div class="row">
                  <div>
                    <form>
                      <div>
                        <p id="new">Add image here (optional)</p>
                        <input type="file" accept="image/*" multiple="multiple" @change="previewMultiImage" class="form-control-file" id="my-file">
                          <template v-if="preview_list.length" >
                          <div>
                              <div v-for="item, index in preview_list" :key="index" class="allList">
                                <div id="item">
                                  <img :src="item" class="img-fluid"/>
                                  <div style="display:flex; justify-content:space-between">
                                  <p style="font-size:9px" class="mb-0">{{ image_list[index].name.substring(0, 5) }}..png</p>
                                  <p style="font-size:9px">{{ (image_list[index].size/1024).toFixed(2) }}KB</p></div>
                                </div>
                              </div>
                          </div>
                          <button @click="reset" id="clear">Clear All</button>
                          </template>
                      </div>
                    </form>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button id="addPostButtton">Add post</button>
          </div>
        </div>
      </div>
    </div>

  </div>

  <div class="carte2">
    <div class="titre">
      <img src="../../assets/follow-up.png" alt="" width="25">
      <h2 style="padding:8px">My followers</h2>
    </div>
    <hr>
    <div class="followers" v-for="follower in followers" :key="follower.id">
      <div class="follower">
        <div>
          <img src="https://static.vecteezy.com/system/resources/previews/019/879/186/non_2x/user-icon-on-transparent-background-free-png.png" alt="" width="50">
          <span>{{ follower.foll }}</span>
        </div>
          <img src="../../assets/details.png" alt="" width="20" align="center" style="cursor:pointer; margin-top:-5px">
      </div>
    </div>
  </div>
  </section>
</template>

<script>
export default {
data() {
    return {
      preview: null,
      image: null,
      preview_list: [],
      image_list: [],
      data:[
        { id: 1, post: "Lorem ipsum dolor sit amets...", like: 10 },
        { id: 2, post: "Lorem ipsum dolor sit amet...", like: 30 },
        { id: 3, post: "Ipsum dolor sit amet...", like: 13 },
      ],followers:[
        { id: 1, foll: "Bill GATES"},
        { id: 2, foll: "Josh BROLLIN"},
        { id: 3, foll: "Scarlet Johanson"},
        { id: 4, foll: "Bill GATES"},
        { id: 5, foll: "Josh BROLLIN"}
      ]
    };
  },
  methods: {
    previewMultiImage: function(event) {
      var input = event.target;
      var count = input.files.length;
      var index = 0;
      if (input.files) {
        while(count --) {
          var reader = new FileReader();
          reader.onload = (e) => {
            this.preview_list.push(e.target.result);
          }
          this.image_list.push(input.files[index]);
          reader.readAsDataURL(input.files[index]);
          console.log(this.all_images)
          index ++;
        }
        console.log(this.preview_list)
      }
    },
    reset: function() {
      this.image = null;
      this.preview = null;
      this.image_list = [];
      this.preview_list = [];
    }
  }
}

// const data = [
//   { id: 1, post: "Lorem ipsum dolor sit amets...", like: 10 },
//   { id: 2, post: "Lorem ipsum dolor sit amet...", like: 30 },
//   { id: 3, post: "Ipsum dolor sit amet...", like: 13 },
// ];
// const followers = [
//   { id: 1, foll: "Bill GATES"},
//   { id: 2, foll: "Josh BROLLIN"},
//   { id: 3, foll: "Scarlet Johanson"},
//   { id: 4, foll: "Bill GATES"},
//   { id: 5, foll: "Josh BROLLIN"}
// ];
</script>

<style>
#clear{
  position: absolute;
  top: 241px;
  right: 20px;
  background-color: rgb(98, 98, 220);
  border: none;
  width: 110px;
  padding: 5px;
  border-radius: 5px;
}
#new{
  margin-bottom: -25px;
  font-size: 13px;
  border: 1px solid #0000002c;
  border-radius: 5px;
  padding: 10px;
}
#my-file{
  opacity: 0;
}
.allList{
  display:inline-flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 10px;
}
#item{
  width: 145px;
  border: 1px solid #0000002c;
  padding: 5px;
  border-radius: 7px;
  margin-right: 10px;
}
#tArea{
  background-color: transparent;
  border: 1px solid rgb(150, 150, 151);
  resize: none;
  border-radius: 10px;
  overflow-y: scroll;
  width: 100%;
  color: #000;
  padding: 5px;
  outline: none;
}
#addPostButtton{
  border: none;
  background-color: rgb(98, 98, 220);
  padding: 10px;
  width: 150px;
  font-weight: bold;
  border-radius: 5px;
}
.carte, .carte2{
  /* width: 20%; */
  background-color: #fff;
  margin: 20px;
  border-radius: 10px;
  overflow-y: scroll;
  color: #000;
}
.topcarte {
  background-color: rgb(98, 98, 220);
  height: 80px;
  width: 100%;
  overflow: hidden;
}
#profile {
  margin-top: -40px;
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-left: 100px;
  border: 4px solid #fff;
  border-radius: 50%;
}
.bottomcarte h2 {
  text-align: center;
  font-size: 15px;
  margin-top: -4px;
}
#email {
  text-align: center;
  font-size: 14px;
  margin-top: -10px;
}
#citation {
  text-align: center;
  margin: auto;
  padding: 30px;
  margin-top: -35px;
  font-size: 12px;
}
hr {
  margin-top: -15px;
  border: 1px solid #0000002c;
}
.post,
.like {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.lastPost {
  margin: 30px;
}
.post {
  margin-top: -30px;
  margin-bottom: -30px;
  font-size: 12px;
  text-align: justify;
  padding-top: 5px;
  padding-bottom: 5px;
  line-height: 5px;
  cursor: pointer;
}
.like p {
  margin-right: 10px;
  color: rgb(98, 98, 220);
  font-weight: bold;
}
.update img,
.addPost img {
  margin-right: 10px;
  transition: ease-in-out 0.3s;
}
.update,
.addPost {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: auto;
  width: 70%;
  border: 1px solid rgb(98, 98, 220);
  border-radius: 30px;
  margin-bottom: 20px;
  cursor: pointer;
  height: 40px;
  margin-top: 20px;
  transition: ease-in-out 0.2s;
}
.update:hover.update img,
.addPost:hover.addPost img {
  display: none;
}
.update:hover,
.addPost:hover {
  background-color: rgb(98, 98, 220);
  color: #fff;
}
.carte2{
  height: 150px;
  overflow-y: scroll;
}
.titre{
  display: flex;
  justify-content: center;
  align-items: center;
}
.titre h2{
  font-size: 17px;
  color: rgb(98, 98, 220);
  font-weight: bold;
  margin-left: 15px;
}
.follower{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-left: 15px;
  margin-right: 30px;
  color: rgb(25, 36, 8);
  cursor: pointer;
  margin-top: 15px;
}
.follower:hover{
  opacity: .5;
}
.follower div{
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 10px;
}
.carte2 hr{
  margin: 20px;
  border-radius: 10px;
  margin-top: -1px;
}
.buttons p{
  margin-bottom: 0px;
}
</style>

<template>
  <section id="cartes">
  <div class="carte">
    <div class="topcarte"></div>
    <img v-if="profile === 'null'" id="profile" src="../../assets/profil.png" alt="" width="90" style="margin-right:100px"/>
    <img v-else :src="profile" alt="" width="90">
    <div class="bottomcarte">
      <h2>@{{ username }}</h2>
      <p id="email">{{email}}</p>
      <p id="citation" v-if="citation !== 'null'">{{ citation }}</p>
      <p id="citation"></p>

    </div>
    <hr />
    <p style="height:2px"></p>
    <!-- <div class="lastPost" v-for="post in data" :key="post.id">
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
    <hr /> -->
    <div class="buttons">
      <!-- <router-link to="/profile">
        <div class="update">
          <img src="../../assets/update.png" alt="" width="17" />
          <p>Update profile</p>
        </div>
      </router-link> -->
      <div class="addPost" data-toggle="modal" data-target="#addPost">
        <img src="../../assets/plus.png" alt="" width="17" />
        <p>Add new post</p>
      </div>
      <!-- <div class="addPost" @click="setAll">
        <p>{{ view }}</p>
      </div> -->
    </div>

    <!-- Modal -->
    <div class="modal fade" id="addPost" tabindex="-1" role="dialog" aria-labelledby="addPostCentertitre" aria-hidden="true" ref="addPostModal">

      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content" >
          <div class="modal-header">
            <h5 class="modal-titre" id="addPostLongtitre">Add new post</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div v-if="message !== ''" class="alert alert-success alert-dismissible fade show" role="alert">
            <strong>{{ message }}</strong>
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <div class="postArea">
              <p style="font-size:13px; margin-bottom:0px">Your article here</p>
              <textarea id="tArea" rows="10" v-model="post"></textarea>
            </div>
            <!-- <div class="imageFac">
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
            </div> -->
          </div>



          <div class="modal-footer">
            <button id="addPostButtton" @click="addPost">Add post</button>
          </div>
        </div>
      </div>
    </div>
</div>
  </section>
</template>

<script>
import base_url from '../../constant';
export default {
  data() {
    return {
      base_url:base_url,
      preview: null,
      image: null,
      image_list:[],
      post:"",
      preview_list: [],
      data:[
        { id: 1, post: "Lorem ipsum dolor sit amets...", like: 10 },
        { id: 2, post: "Lorem ipsum dolor sit amets...", like: 30 },
        { id: 3, post: "Ipsum dolor sit amets...", like: 13 },
      ],
      username : sessionStorage.getItem('username'),
      email : sessionStorage.getItem('email'),
      token : sessionStorage.getItem('token'),
      profile : sessionStorage.getItem('profile'),
      citation : sessionStorage.getItem('citation'),
      message :"",
      view:"View all posts"
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
          index ++;
        }
      }
    },
    reset: function() {
      this.image = null;
      this.preview = null;
      this.image_list = [];
      this.preview_list = [];
    },
    addPost:function() {
        const data = {
          email:sessionStorage.getItem('email'),
          post: this.post
        };
        const options = {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        };
        fetch(`${this.base_url}/add-posts`, options)
        .then(response => response.json())
        .then(jsonData => {
          if (jsonData.success) {
            this.message = jsonData.message
            console.log(jsonData); 
            // this.$refs.addPostModal.hide();
            window.location.reload()
          }
        })
        .catch(error => {
          console.log('Error:', error);
          this.message = jsonData.message
        });
      },
      setAll: function() {
        if(localStorage.getItem('view_all') !== null) {
          localStorage.getItem('view_all') === 'true' ? localStorage.setItem('view_all', 'false') : localStorage.setItem('view_all', 'true');
          window.location.reload()
        }
      }
    }
  }

</script>

<style>
#cartes{
  height: 91vh;
  overflow: hidden;
}
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
.carte{
  height: 88vh;
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
  height: 186px;
  overflow-y: scroll;
  display: none;
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

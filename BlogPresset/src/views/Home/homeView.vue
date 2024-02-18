<script setup>
import AppMenu from "../../components/AppMenu.vue";
import LeftSideView from "../../components/home/LeftSideView.vue";
import RightSideView from "../../components/home/RightSideView.vue";
// import test from "./constant/index";
// const tes = test.test;

const articles = [
  {
    id:1,
    author: "@Pseudo1",
    post: "When referring to article,it can have different meanings depending on the context. In general, it can signify a piece of writing in a newspaper, magazine, or online publication, as defined in the Cambridge English Dictionar",
    citation: "lorem ipsum dolor...",
    image: [
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTu34O52K_RgeZL7kjalkKhiCL48Sz7WoYFcg&usqp=CAU",
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTu34O52K_RgeZL7kjalkKhiCL48Sz7WoYFcg&usqp=CAU",
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTu34O52K_RgeZL7kjalkKhiCL48Sz7WoYFcg&usqp=CAU",
    ],
  },
  {
    id:2,
    author: "@Mélène TONOU",
    post: "When referring to article,it can have different meanings depending on the context. In general, it can signify a piece of writing in a newspaper, magazine, or online publication, as defined in the Cambridge English Dictionar",
    citation: "lorem ipsum dolor...",
    image: [
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTu34O52K_RgeZL7kjalkKhiCL48Sz7WoYFcg&usqp=CAU",
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTu34O52K_RgeZL7kjalkKhiCL48Sz7WoYFcg&usqp=CAU",
    ],
  },
  {
    id:3,
    author: "@Mélène TONOU",
    post: "When referring to article,it can have different meanings depending on the context. In general, it can signify a piece of writing in a newspaper, magazine, or online publication, as defined in the Cambridge English Dictionar",
    citation: "lorem ipsum dolor...",
    image: [
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTu34O52K_RgeZL7kjalkKhiCL48Sz7WoYFcg&usqp=CAU",
    ],
  },
  {
    id:4,
    author: "@Mélène TONOU",
    post: "When referring to article,it can have different meanings depending on the context. In general, it can signify a piece of writing in a newspaper, magazine, or online publication, as defined in the Cambridge English Dictionar",
    citation: "lorem ipsum dolor...",
    image: [],
  },
];
</script>

<template>
  <section id="container">
    <AppMenu :act="1" />
    <section id="corps">
      <LeftSideView />
      <section id="blog">
        <div class="userCard"></div>
        <div class="articles" v-for="article in articles" :key="article.id">
          <div class="article">
            <div class="author">
              <div class="image">
                <img src="../../assets/profil.png" alt="" width="50" style="margin-top:-6px">
              </div>
              <div class="userInfo">
                <h2>@Pseudo{{ article.id }}</h2>
                <p>{{ article.citation }}</p>
              </div>
            </div>
              <div class="userPost">
                <p>{{ article.post }}</p>
              </div>
              <div class="userPostImage">
                <div v-if="article.image.length === 1" class="oneImage">
                  <img :src="article.image[0]" alt="">
                </div>
                <div v-if="article.image.length === 2" class="twoImage">
                  <img :src="article.image[0]" alt="">
                  <img :src="article.image[1]" alt="">
                </div>
                <div v-if="article.image.length === 3" class="threeImage">
                  <img id="one" :src="article.image[0]" alt="">
                  <div>
                  <img id="two" :src="article.image[1]" alt=""> <br>
                  <img id="three" :src="article.image[2]" alt="">
                  </div>
                </div>
              </div>

              <div class="reactions">
                <div id="pouce">
                  <img src="../../assets/like.png" alt="" width="22">
                  <img src="../../assets/share.png" alt="" width="22">
                  <img src="../../assets/messager.png" alt="" width="22">
                </div>
                <div class="all">
                  <p>All comments</p>
                </div>
              </div>
            
          </div>
        </div>
      </section>
      <RightSideView />
    </section>

    <router-view />
  </section>
</template>

<style>
#corps {
  display: flex;
  width: 100%;
  flex-direction: row;
  overflow: hidden;
}
#blog {
  width: 55%;
  background-color: #fff;
  margin-top: 20px;
  height: 88vh;
  overflow: scroll;
  color: #000;
  border-radius: 10px;
}
.article{
  padding: 20px;
  margin: 20px;
  border: 1px solid #d7d7d7;
  border-radius: 10px;
}
.author{
  display: flex;
  justify-content: flex-start;
  align-items: center;
}
.userInfo h2{
  margin-left: 10px;
  font-size: 15px;
  margin-top: -3px;
}
.userInfo p{
  font-size: 12px;
  margin-top: -10px;
  margin-left: 10px;
}
.userPost p{
  text-align: justify;
  font-size: 15px;
}
.threeImage, .oneImage, .twoImage{
  display: flex;
  justify-content: center;
  align-items: center;
}
#one{
  width: 260px;
  margin-right: 40px;
  margin-bottom: 20px;
}
#two, #three{
  width: 120px;
  margin-left: 40px;
  margin-bottom: 20px;

}
.twoImage img, .oneImage img{
  width: 120px;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}
.reactions{
  display: flex;
  justify-content: space-between;
  align-items: center;
}
#pouce img{
  margin-right: 40px;
  cursor: pointer;
}
.all p{
  cursor: pointer;
  color: rgb(98, 98, 220);
}

#pouce img:hover, .all p:hover{
  opacity: .5;
  color: #787878;
}
</style>

<template>
  <section>
  <div class="card">
    <div class="bottomCard">
      <h2>@John Doe</h2>
      <p id="email">test@gmail.com</p>
      <p id="citation">"Lorem ipsum dolor sit amet consectetur"</p>
    </div>
  </div>
  </section>
</template>

<script setup>
const data = [
  { id: 1, post: "Lorem ipsum dolor sit amets...", like: 10 },
  { id: 2, post: "Lorem ipsum dolor sit amet...", like: 30 },
  { id: 3, post: "Ipsum dolor sit amet...", like: 13 },
];
const followers = [
  { id: 1, foll: "Bill GATES"},
  { id: 2, foll: "Josh BROLLIN"},
  { id: 3, foll: "Scarlet Johanson"},
  { id: 4, foll: "Bill GATES"},
  { id: 5, foll: "Josh BROLLIN"}
];
</script>

<style scoped>
.card{
  background-color: #fff;
  margin: 20px;
  border-radius: 10px;
  overflow-y: scroll;
  color: #000;
  height: 88vh;
}
.topCard {
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
.bottomCard h2 {
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
  padding: 5px;
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
.card2{
  height: 200px;
  overflow-y: scroll;
}
.title{
  display: flex;
  justify-content: center;
  align-items: center;
}
.title h2{
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
.card2 hr{
  margin: 20px;
  border-radius: 10px;
  margin-top: -1px;
}
</style>

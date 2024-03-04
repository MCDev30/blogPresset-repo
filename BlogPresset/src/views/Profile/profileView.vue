<script setup>
import base_url from "../../constant/index";
import AppMenu from "../../components/AppMenu.vue";
import { ref, onBeforeMount } from "vue";

const username = sessionStorage.getItem("username");
const email = sessionStorage.getItem("email");
const posts = ref({});

const logout = async () => {
  const data = {
    email: sessionStorage.getItem("email"),
    token: sessionStorage.getItem("token"),
  };
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  };
  try {
    const response = await fetch(`${base_url}/logout`, options);
    const jsonResponse = await response.json();
    if (jsonResponse.status === 200) {
      sessionStorage.clear();
      localStorage.clear();
      window.location.href = "/";
    }
  } catch (error) {
    console.error("Erreur lors de la requête :", error);
    throw error;
  }
};

onBeforeMount(() => {
  fetch(`${base_url}/all_posts_with_comments`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      const new_data = [];
      const view = localStorage.getItem("view_all")
        ? localStorage.getItem("view_all")
        : "false";
      let len = 0;
      if (data.total_posts * 1 > 5) {
        if (view === "false") {
          len = 5;
        } else {
          len = data.total_posts * 1;
        }
      } else {
        len = data.total_posts * 1 > 5;
      }
      for (let i = 0; i < data.total_posts * 1; i++) {
        new_data.push(data.all_posts_with_comments[`post${i + 1}`]);
      }
      posts.value = new_data.reverse();
    })
    .catch((error) => {
      console.error("Error fetching posts with comments:", error);
    });
  // console.log(posts.value);
});

const deletePost = (id) => {
  fetch(`${base_url}/delete_post/${sessionStorage.getItem("email")}/${id}`, {
    method: "DELETE",
  })
    .then((response) => {
      if (response.ok) {
        alert("Post deleted successfully");
        window.location.reload();
      } else {
        alert("Failed to delete post. Try again !!");
      }
    })
    .catch((error) => {
      console.error("Error deleting post:", error);
      alert("An error occurred while deleting the post");
    });
};

const deleteAccount = () => {
  const email = sessionStorage.getItem("email");
  const token = sessionStorage.getItem("token");

  fetch(`${base_url}/delete-account`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, token }),
  })
    .then((response) => {
      if (response.ok) {
        alert("Account deleted successfully");
        window.location.href = "/";
      } else {
        alert("Failed to delete account. Try again !!");
      }
    })
    .catch((error) => {
      console.error("Error deleting account:", error);
      alert("An error occurred while deleting the account");
    });
};
</script>

<template>
  <section id="container">
    <AppMenu :act="2" />
    <section id="corps">
      <section id="profil">
        <div class="banniere"></div>
        <div class="img">
          <img src="../../assets/profil.png" alt="" width="150" />
        </div>

        <div class="cont">
          <div class="infos">
            <h2 style="font-size: 16px">@{{ username }}</h2>
            <h4 style="font-size: 16px">{{ email }}</h4>
          </div>
          <div class="langue">
            <p style="font-weight: bold">Profil language</p>
            <p style="margin-top: -15px; color: blue">English</p>
          </div>
          <div class="buttons" style="display: flex">
            <button @click="logout">Logout</button>
            <button @click="deleteAccount" style="background-color: red">
              Delete account
            </button>
          </div>
        </div>

        <div class="posts">
          <h3 style="margin-left: 20px">My all posts</h3>
          <div class="conte" v-if="posts !== {}">
            <div class="single_post" v-for="post in posts" :key="post">
              <div class="use" v-if="post.email === email">
                <p
                  style="
                    position: relative;
                    margin-left: 98%;
                    font-size: 22px;
                    color: red;
                    cursor: pointer;
                  "
                  @click="deletePost(post.post_id)"
                >
                  &times;
                </p>
                <p style="padding:10px; margin-top:-20px">{{ post.post.slice(0, 150) + "..." }}</p>
                <p v-if="post.comments.length !== 0" style="font-size:11px; text-align:right">
                  {{ post.comments.length }} comments for this post
                </p>
                <p v-else style="font-size:11px; text-align:right">{{ post.comments.length }} comment for this post</p>
              </div>
            </div>
          </div>
          <div v-else>
            <p style="font-size:20px; opacity:.5; text-align:center; margin-top:60px">Nothing to show now</p>
          </div>
        </div>
      </section>
      <router-view />
    </section>
  </section>
</template>

<style scoped>
.use {
  background-color: #fff;
  padding: 5px;
  border-radius: 7px;
  margin: 20px;
}
.cont {
  display: flex;
  justify-content: space-between;
  padding: 20px;
}
.cont div {
  background-color: #fff;
  padding: 10px;
  border-radius: 10px;
  width: 31%;
  overflow: hidden;
  height: 70px;
}
button {
  width: 45%;
  margin-top: 10px;
  border: none;
  background-color: blue;
  margin: 10px;
  padding: 5px;
  height: 35px;
  border-radius: 5px;
  cursor: pointer;
}
.banniere {
  background: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQn6keEUZeoJdUJpAPf2bRHbZz2kAudJ873uL5TFzxP&s");
  height: 230px;
  width: 100%;
  background-size: cover;
  background-repeat: no-repeat;
}
.img img {
  margin-top: -100px;
  margin-left: 30px;
  border: 7px solid #fff;
  border-radius: 50%;
}
#corps {
  padding-left: 200px;
  padding-right: 200px;
}
#profil {
  background-color: #ebebeb;
  margin-top: 20px;
  height: 88vh;
  overflow: scroll;
  color: #000;
  border-radius: 10px;
  margin-left: 0px;
}
</style>

<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-1">
            <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">

                <img :src="user.get_avatar" class="mb-6 rounded-full">

                <p><strong>{{ user.name }}</strong></p>
                <p><strong>{{ user.email }}</strong></p>

                <div class="mt-6 flex space-x-8 justify-around" v-if="user.id">
                    <RouterLink :to="{name: 'friends', params: {id: user.id}}" class="text-xs text-gray-500">{{ user.friends_count }} друзья</RouterLink>
                    <p class="text-xs text-gray-500">{{ user.posts_count }} посты</p>
                </div>

                <div class="mt-4">

                    <button 
                        class="inline-block py-4 px-3 bg-purple-600 text-xs text-white rounded-lg" 
                        @click="sendFriendshipRequest"
                        v-if="userStore.user.id !== user.id && can_send_friendship_request"
                    >
                        Запрос на дружбу
                    </button>
                    
                    <br>

                    <button 
                        class="inline-block mt-2 py-4 px-3 bg-purple-600 text-xs text-white rounded-lg" 
                        @click="sendDirectMessage"
                        v-if="userStore.user.id !== user.id"
                    >
                        Отправить сообщение
                    </button>


                    <RouterLink 
                        class="inline-block py-4 px-3 bg-purple-600 text-xs text-white rounded-lg" 
                        to="/profile/edit"
                        v-if="userStore.user.id === user.id"
                    >
                        Редактировать профиль
                    </RouterLink>

                    <br>

                    <button 
                        class="inline-block mt-2  py-4 px-3 bg-red-600 text-xs text-white rounded-lg" 
                        @click="logout"
                        v-if="userStore.user.id === user.id"
                    >
                        Выйти
                    </button>


                </div>
            </div>
        </div>

        <div class="main-center col-span-2 space-y-4">
            <div 
                class="bg-white border border-gray-200 rounded-lg"
                v-if="userStore.user.id === user.id"
            >
                <form v-on:submit.prevent="submitForm" method="post">
                    <div class="p-4">  
                        <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="Пишите что-нибудь"></textarea>


                        <div id="preview" v-if="url">
                            <img :src="url" class="w-[100px] mt-3 rounded-xl" />
                        </div>

                        <div id="preview" v-if="url">
                            <video controls class="w-[100px] mt-3 rounded-xl">
                                <source :src="url" type="video/mp4">
                            </video>
                        </div>

                    </div>

                    <div class="p-4 border-t border-gray-100 flex justify-between">
                        <label class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">
                            <input type="file" ref="file" @change="onFileChange">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M9 3.75H6.912a2.25 2.25 0 00-2.15 1.588L2.35 13.177a2.25 2.25 0 00-.1.661V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18v-4.162c0-.224-.034-.447-.1-.661L19.24 5.338a2.25 2.25 0 00-2.15-1.588H15M2.25 13.5h3.86a2.25 2.25 0 012.012 1.244l.256.512a2.25 2.25 0 002.013 1.244h3.218a2.25 2.25 0 002.013-1.244l.256-.512a2.25 2.25 0 012.013-1.244h3.859M12 3v8.25m0 0l-3-3m3 3l3-3" />
                            </svg>
                        </label>

                        <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
                            </svg>
                        </button>
                    </div>
                </form>
            </div>

            <div 
                class="p-4 bg-white border border-gray-200 rounded-lg"
                v-for="post in posts"
                v-bind:key="post.id"
            >
                <FeedItem v-bind:post="post" v-on:deletePost="deletePost"/>
            </div>
        </div>

        <div class="main-right col-span-1 space-y-4">
            <Trends />

            <!-- REPOSTS -->
            <div class="p-4 bg-white border border-gray-200 rounded-lg" v-if="userStore.user.id === user.id">
                <h3 class="mb-6 text-xl"><strong>Мои репосты</strong></h3>
                <div 
                    class="p-4 bg-gray border border-gray-200 rounded-lg mb-2"
                    v-for="repost in reposts"
                    :key="repost.id"
                >
                    <div class="mb-6 flex items-center justify-between">
                        <div class="flex items-center space-x-6">
                            <img :src="repost.original_post.created_by.get_avatar" class="w-[40px] rounded-full">
                            <p>
                                <strong>
                                    <RouterLink :to="{name: 'profile', params:{'id': repost.original_post.created_by.id}}">{{ repost.original_post.created_by.name }}</RouterLink>
                                </strong>
                            </p>
                        </div>

                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z"></path>
                        </svg> 
                    </div>

                    <template v-if="repost.original_post.attachments.length">
                        <!-- <img v-for="image in repost.original_post.attachments" v-bind:key="image.id" :src="image.get_file" class="w-full mb-2 rounded-xl"> -->
                        <template v-for="attachment in repost.original_post.attachments">
                            <template v-if="isImage(attachment.get_file)">
                                <img :src="attachment.get_file" class="w-full mb-4 rounded-xl">
                            </template>
                            <template v-else-if="isVideo(attachment.get_file)">
                                <video controls class="w-full mb-4 rounded-xl">
                                    <source :src="attachment.get_file">
                                    Ваш браузер не поддерживает видео.
                                </video>
                            </template>
                        </template>
                    </template>
                    
                    <p>{{ repost.original_post.body }}</p>
                    <div class="my-2 flex justify-between">
                        <div class="flex space-x-6">
                            <div class="flex items-center space-x-2" @click="likePost(repost.original_post.id)">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z"></path>
                                </svg>  
                                
                                <span class="text-gray-500 text-xs">{{ repost.original_post.likes_count }} лайков</span>
                            </div>
                            
                            <div class="flex items-center space-x-2">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 01-.923 1.785A5.969 5.969 0 006 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337z"></path>
                                </svg> 

                                <RouterLink :to="{name: 'postview', params: {id: repost.original_post.id}}" class="text-gray-500 text-xs">{{ repost.original_post.comments_count }} комментов</RouterLink>
                            </div>
                        </div>
                    </div>
                </div>  
            </div>
             <!-- END_REPOSTS -->

        </div>
    </div>
</template>


<style>
input[type="file"] {
    display: none;
}

.custom-file-upload {
    border: 1px solid #ccc;
    display: inline-block;
    padding: 6px 12px;
    cursor: pointer;
}
</style>


<script>
import axios from 'axios'
import Trends from '../components/Trends.vue'
import FeedItem from '../components/FeedItem.vue'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import { RouterLink } from 'vue-router'

export default {
    name: 'FeedView',
    emits: ['deletePost'],

    setup() {
        const userStore = useUserStore()
        const toastStore = useToastStore()

        return {
            userStore,
            toastStore
        }
    },

    components: {
        Trends,
        FeedItem,
        RouterLink
    },

    data() {
        return {
            posts: [],
            reposts: [],
            user: {
                id: ''
            },
            can_send_friendship_request: null,
            body: '',
            url: null,
            
        }
    },

    mounted() {
        this.getFeed()
    },


    watch: { 
        '$route.params.id': {
            handler: function() {
                this.getFeed()
            },
            deep: true,
            immediate: true
        }
    },

    methods: {
        deletePost(id) {
            this.posts = this.posts.filter(post => post.id !== id)
            this.user.posts_count -= 1
        },

        onFileChange(e) {
            const file = e.target.files[0];
            this.url = URL.createObjectURL(file);
        },

        likePost(id) {
            axios
                .post(`/api/posts/${id}/like/`)
                .then(response => {
                    if (response.data.message === "like created") {
                        this.post.likes_count += 1;
                    }
                })
                .catch(error => {
                    console.log("error", error);
                });
        },

        sendDirectMessage() {
            console.log('sendDirectMessage')

            axios
                .get(`/api/chat/${this.$route.params.id}/get-or-create/`)
                .then(response => {
                    console.log(response.data)

                    this.$router.push('/chat')
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        sendFriendshipRequest() {
        axios
            .post(`/api/friends/${this.$route.params.id}/request/`)
            .then(response => {
                console.log('data', response.data)

                this.can_send_friendship_request = false

                if (response.data.message == 'request already sent') {
                    this.toastStore.showToast(5000, 'The request has already been sent!', 'bg-red-300')
                } else {
                    this.toastStore.showToast(5000, 'The request was sent!', 'bg-emerald-300')
                }
            })
            .catch(error => {
                console.log('error', error)
            })
        },

        getFeed() {
            axios
                .get(`/api/posts/profile/${this.$route.params.id}/`)
                .then(response => {
                    console.log('data', response.data)

                    this.posts = response.data.posts
                    this.reposts = response.data.reposts  
                    this.user = response.data.user
                    this.can_send_friendship_request = response.data.can_send_friendship_request

                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        submitForm() {
            if (!this.body.trim()) {
                return;
            }

            console.log('submitForm', this.body)

            let formData = new FormData()
            formData.append('file', this.$refs.file.files[0])
            formData.append('body', this.body)

            axios
                .post('/api/posts/create/', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    }
                })
                .then(response => {
                    console.log('data', response.data)

                    this.posts.unshift(response.data)
                    this.body = ''
                    this.$refs.file.value = null
                    this.url = null
                    this.user.posts_count += 1
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        logout() {
            console.log('Log out')
            this.userStore.removeToken()
            this.$router.push('/login')
        },

        isImage(url) {
            const imageExtensions = ['jpg', 'jpeg', 'png', 'gif'];
            const extension = url.split('.').pop().toLowerCase();
            return imageExtensions.includes(extension);
        },

        isVideo(url) {
            const videoExtensions = ['mp4', 'avi', 'mkv', 'mov'];
            const extension = url.split('.').pop().toLowerCase();
            return videoExtensions.includes(extension);
        },
    }
}

</script>



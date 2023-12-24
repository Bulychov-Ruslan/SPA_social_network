<!-- views/FeedView.vue -->
<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-center col-span-3 space-y-4">
            <div class="bg-white border border-gray-200 rounded-lg">
                
                <!-- FORM -->
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
                <!-- END_FORM -->
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

export default {
    name: 'FeedView',
    emits: ['deletePost'],

    components: {
        FeedItem,
        Trends,
    },

    data() {
        return {
            posts: [],
            body: '',
            url: null,
        }
    },

    mounted() {
        this.getFeed()
    },

    methods: {
        onFileChange(e) {
            const file = e.target.files[0];
            this.url = URL.createObjectURL(file);
        },

        getFeed() {
            axios
                .get('/api/posts/')
                .then(response => {
                    console.log('data', response.data)
                    this.posts = response.data
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        deletePost(id) {
            this.posts = this.posts.filter(post => post.id !== id)
            this.posts.posts_count -= 1
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
                })
                .catch(error => {
                    console.log('error', error)
                })
        },
    }
}
</script>




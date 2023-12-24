<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-center col-span-3 space-y-4">

            <div 
                class="p-4 bg-white border border-gray-200 rounded-lg"
                v-if="post.id"
            >
                <FeedItem v-bind:post="post" v-on:deletePost="deletePost" />
            </div>

            <div
                class="p-4 ml-6 bg-white border border-gray-200 rounded-lg"
                v-for="comment in post.comments"
                v-bind:key="comment.id"
            >
                <CommentItem v-bind:comment="comment" />
            </div>

            <div class="bg-white border border-gray-200 rounded-lg">
                <form v-on:submit.prevent="submitForm" method="post">
                    <div class="p-4">  
                        <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="Добавить комментарий!"></textarea>
                    </div>

                    <div class="p-4 border-t border-gray-100">
                        <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
                            </svg>
                        </button>
                    </div>
                </form>
            </div>
        </div>

        <div class="main-right col-span-1 space-y-4">
            <Trends />
        </div>
    </div>
</template>


<script>
import axios from 'axios'
import Trends from '../components/Trends.vue'
import FeedItem from '../components/FeedItem.vue'
import CommentItem from '../components/CommentItem.vue'

export default {
    emits: ['deletePost'],
    name: 'PostView',

    components: {
        Trends,
        FeedItem,
        CommentItem
    },

    data() {
        return {
            post: {
                id: null,
                comments: []
            },
            body: ''
        }
    },

    mounted() {
        this.getPost()
    },

    methods: {
        getPost() {
            axios
                .get(`/api/posts/${this.$route.params.id}/`)
                .then(response => {
                    console.log('data', response.data)

                    this.post = response.data.post
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

            axios
                .post(`/api/posts/${this.$route.params.id}/comment/`, {
                    'body': this.body
                })
                .then(response => {
                    console.log('data', response.data)

                    this.post.comments.push(response.data)
                    this.post.comments_count += 1
                    this.body = ''
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        deletePost(id) {
            this.posts = this.posts.filter(post => post.id !== id)
            this.$router.push('/feed')

        },
    }
}
</script>
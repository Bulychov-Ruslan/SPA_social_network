<template>
    <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">

        <div class="main-left">

            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <h1 class="mb-6 text-2xl"><strong>Регистрация</strong></h1>

                <p class="mb-6 text-gray-500">
                    Здесь вы можете зарегистрировать новую учетную запись!
                </p>

                <p class="font-bold">
                    У вас уже есть аккаунт? Кликните <RouterLink :to="{'name': 'login'}" class="underline">здесь</RouterLink> чтобы войти!
                </p>
            </div>

        </div>

        <div class="main-right">

            <div class="p-12 bg-white border border-gray-200 rounded-lg">

                <form class="space-y-6" v-on:submit.prevent="submitForm">
                    <div>
                        <label>Имя</label><br>
                        <input type="text" v-model="form.name" placeholder="Ваше полное имя" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <div>
                        <label>E-mail</label><br>
                        <input type="email" v-model="form.email" placeholder="Ваш электронный адрес" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <div>
                        <label>Пароль</label><br>
                        <input type="password" v-model="form.password1" placeholder="Введите пароль" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <div>
                        <label>Повторите пароль</label><br>
                        <input type="password" v-model="form.password2" placeholder="Повторите пароль" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <template v-if="errors.length > 0">
                        <div class="bg-red-300 text-white rounded-lg p-6">
                            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                        </div>
                    </template>

                    <div>
                        <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">Регистрация</button>
                    </div>

                </form>

            </div>
        </div>
    </div>
</template>


<script>
import axios from 'axios'
import { useToastStore } from '@/stores/toast'

export default {
    setup() {
        const toastStore = useToastStore()

        return {
            toastStore
        }
    },

    data() {
        return {
            form: {
                email: '',
                name: '',
                password1: '',
                password2: ''
            },
            errors: [],
        }
    },

    methods: {
        submitForm() {
            this.errors = []

            if (this.form.email === '') {
                this.errors.push('Ваш адрес электронной почты отсутствует')
            }

            if (this.form.name === '') {
                this.errors.push('Ваше имя отсутствует')
            }

            if (this.form.password1 === '') {
                this.errors.push('Ваш пароль отсутствует')
            }

            if (this.form.password1 !== this.form.password2) {
                this.errors.push('Пароль не соответствует ранне введенному паролю')
            }

            if (this.errors.length === 0) {
                axios
                    .post('/api/signup/', this.form)
                    .then(response => {
                        if (response.data.message === 'success') {
                            this.toastStore.showToast(5000, 'Пользователь зарегистрирован. Пожалуйста, войдите', 'bg-emerald-500')

                            this.form.email = ''
                            this.form.name = ''
                            this.form.password1 = ''
                            this.form.password2 = ''

                            this.$router.push('/login')
                        } else {
                            const data = JSON.parse(response.data.message)
                            for (const key in data){
                                this.errors.push(data[key][0].message)
                            }


                            this.toastStore.showToast(5000, 'Что-то пошло не так. Пожалуйста, попробуйте еще раз', 'bg-red-300')
                        }
                    })
                    .catch(error => {
                        console.log('error', error)
                    })
            }
        }
    }
}
</script>
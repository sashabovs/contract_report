
import Token from './Token.js'

export default {
    components: {
    },
    data() {
        return {
            loginVal: "",
            passwordVal: "",
        };
    },
    methods: {
        login(){
            const body = {"login": this.loginVal, "password": this.passwordVal}
            axios.post('/login', body)
            .then((res) => {
                Token.token = res.data.token
                var tokens = this.token.split(".");
                var token_data = JSON.parse(atob(tokens[1]));

                if(token_data.role === 'administrator'){
                    this.$router.push('/admin');
                }
            })
            .catch((error) => {
              console.log(error.data.message)
            })

        }
    },
    template: `
        <div>
            <label for="login">Login:</label>
            <input id="login" required v-model="loginVal">
            <label for="password">Password:</label>
            <input id="password" required v-model="passwordVal">
            <button v-on:click="login">Login</button>
        </div>
    `,
};
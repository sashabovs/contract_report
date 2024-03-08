
import Token from './Token.js'

export default {
    components: {
    },
    data() {
        return {
            loginVal: "muxina",
            passwordVal: "123",
        };
    },
    methods: {
        login(){
            const body = {"login": this.loginVal, "password": this.passwordVal}
            axios.post('/login', body)
            .then((res) => {
                Token.token = res.data.token
                var tokens = Token.token.split(".");
                var token_data = JSON.parse(atob(tokens[1]));

                if(token_data.role === 'administrator'){
                    this.$router.push('/admin');
                }else if(token_data.role === 'head_of_human_resources'){
                    this.$router.push('/head_of_human_resources');
                }
            })
            .catch((error) => {
              console.log(error.response.data)
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
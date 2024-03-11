
export default {
  token: "",
  getTokenData:function (){
    var tokens = this.token.split(".");
    return JSON.parse(atob(tokens[1]));
  }
};

<template>
  <div id="app">
    <div id="nav">
      <h1>News</h1>
      <div class="infos">
        <label>Always remember to use this hotkeys:</label>
        <p>-> 1 : Good News</p>
        <p>-> 2 : Bad News</p>
        <p>-> 3 : No Value</p>
        <p>-> 4 : Next News</p>
      </div>
    </div>
    <router-view/>
  </div>
</template>

<style lang="scss">
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
#nav {
  padding: 30px;
  display: flex;
  flex-direction: row;
  justify-content: left;
  & h1 {
    color: #b60000;
    width: 20%;
    margin-left: 40%
  }
  .infos{
    margin-left: 18%;
    width: 20%;
    text-align: left;
  }
}
</style>

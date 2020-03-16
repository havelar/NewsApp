<template>
  <div class="News">
    <div id="UpperPart">
      <div class="title">
        <h1>{{title}}</h1>
      </div>
      <form class="selectPanel" @submit.prevent="AvalieateNLoad">
        <button type="submit" v-if="this.id_ !== ''"  onclick="this.parentNode.value='1'">Noticia Boa</button>
        <button type="submit" v-if="this.id_ !== ''"  onclick="this.parentNode.value='2'">Noticia Ruim</button>
        <button type="submit" v-if="this.id_ !== ''"  onclick="this.parentNode.value='3'">Noticia sem valor</button>
        <button type="submit" v-if="this.id_ !== ''"  onclick="this.parentNode.value='4'">Pular</button>
        <button type="submit" v-if="this.id_ !== ''"  onclick="this.parentNode.value='5'">Parar</button>
        <button type="submit" v-if="this.id_ === ''"  @click.prevent="LoadLink">Continuar</button>
      </form>
    </div>
    <div class="display">
      <div class="id_">
        <h3>id_</h3>
        <label>{{id_}}</label>
      </div>
      <div class="subTitle">
        <h3>SubTitle</h3>
        <label>{{subTitle}}</label>
      </div>
      <div class="date">
        <h3>Date</h3>
        <label>{{date}}</label>
      </div>
      <div class="link">
        <h3>Link</h3>
        <label>{{link}}</label>
      </div>
      <div class="article">
        <h3>Article</h3>
        <label>{{article}}</label>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'News',
  data () {
    return {
      title: '',
      subTitle: '',
      date: '',
      article: '',
      link: '',
      id_: ''
    }
  },
  methods: {
    async AvalieateNLoad (event) {
      const data = new FormData()
      const status = event.target.value
      data.append('_id', this.id_)
      data.append('status', status)

      if (this.id_ !== '') {
        await fetch('http://192.168.100.144:8000/avaliate_links', {
          method: 'POST',
          body: data
        })
      }

      if (status !== '5') {
        this.LoadLink()
      }

      else {
        this.title = 'Any new news.'
        this.subTitle = ''
        this.link = ''
        this.article = ''
        this.date = ''
        this.id_ = ''
      }
    },
    async LoadLink () {
      console.log('Rolou')
      let response = await fetch('http://192.168.100.144:8000/get_links')

      if (response.status === 200) {
        response = await response.json()

        this.title = response.title
        this.subTitle = response.subtitle
        this.link = response.link
        this.article = response.article
        this.date = response.date
        this.id_ = response.id_
      }
    }
  },
  mounted () {
    this.LoadLink()
  }
}
</script>

<style lang="scss" scoped>

  #UpperPart{
    display: flex;
    .title{
      display: flex;
      width: 100%;
      align-items: center;
      h1{
        text-align: center;
        justify-content: center;
        width: 90%;
      }
    }
    .selectPanel {
      display: flex;
      flex-direction: column;
      height: 200px;
      width: 30%;
      margin-right: 5%;
      justify-content: space-between;
      button {
        height: 25%;
        width: 100%;
      }
    }

    .display{
      display: flex;
      flex-direction: column;

    }
  }
</style>

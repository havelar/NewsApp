<template>
  <div class="News">
    <div id="UpperPart">
      <div class="title">
        <h1>{{title}}</h1>
      </div>
      <div class='status'>
        <h3> Status: </h3>
        <p>Lefts: {{LeftNews}}</p>
        <p>Good: {{GNews}}</p>
        <p>Bad: {{BNews}}</p>
      </div>
      <form class="selectPanel" @submit.prevent="AvalieateNLoad">
        <button type="submit" class="goodButton" v-if="this.id_ !== ''"  onclick="this.parentNode.value='1'">Good News</button>
        <button type="submit" class="badButton" v-if="this.id_ !== ''"  onclick="this.parentNode.value='2'">Bad News</button>
        <button type="submit" class="noValButton" v-if="this.id_ !== ''"  onclick="this.parentNode.value='3'">No Value</button>
        <button type="submit" class="nextButton" v-if="this.id_ !== ''"  onclick="this.parentNode.value='4'">Next</button>
        <button type="submit" class="stopButton" v-if="this.id_ !== ''"  onclick="this.parentNode.value='5'">Stop</button>
        <button type="submit" class="startButton" v-if="this.id_ === ''"  @click.prevent="LoadLink">Start</button>
      </form>
    </div>
    <div id="SubtitlePart" v-if="this.id_ !== ''">
      <h2>{{subTitle}}</h2>
    </div>
    <div id="Date" v-if="this.id_ !== ''">
      <a v-bind:href="this.link">Link</a>
      <p>{{date}}</p>
    </div>
    <div id="Article" v-if="this.id_ !== ''">
      <p>{{article}}</p>
    </div>
    <div class="display" v-if="this.id_ !== ''">
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
      id_: '',
      LeftNews: 0,
      GNews: 0,
      BNews: 0
    }
  },
  methods: {
    async AvalieateNLoad (event) {
      const data = new FormData()
      const status = event.target.value
      data.append('_id', this.id_)
      data.append('status', status)

      if (this.id_ !== '') {
        await fetch('http://192.168.100.142:8000/avaliate_links', {
          method: 'POST',
          body: data
        })
      }

      if (status !== '5') {
        this.LoadLink()
      } else {
        this.title = "Press start to get some new n' tasty news."
        this.subTitle = ''
        this.link = ''
        this.article = ''
        this.date = ''
        this.id_ = ''
      }
    },
    async LoadLink () {
      let response = await fetch('http://192.168.100.142:8000/get_links')
      let resp = await fetch('http://192.168.100.142:8000/get_info')

      if (response.status === 200) {
        response = await response.json()
        resp = await resp.json()

        this.title = (response.title === '') ? 'No Title.' : response.title
        this.subTitle = (response.subtitle === '') ? 'No Subtitles.' : response.subtitle
        this.link = (response.link === '') ? 'google.com.br' : response.link
        this.article = (response.article === '') ? 'No Article.' : response.article
        this.date = (response.date === '') ? 'No Date.' : response.date
        this.id_ = (response.id_ === '') ? 'No Id.' : response.id_

        this.LeftNews = (resp.Rest === '') ? 0 : resp.Rest
        console.log(this.LeftNews)
        console.log('Here')
        this.GNews = (resp.Bom === '') ? 0 : resp.Bom
        this.BNews = (resp.Ruim == '') ? 0 : resp.Ruim
      }
    }
  },
  mounted () {
    if (this.title === ''){
      this.LoadLink()
    }

    window.addEventListener('keyup', e => {
      // console.log(String.fromCharCode(e.keyCode));
      // console.log(e.keyCode)
      if ((e.keyCode === 49 || e.keyCode === 97) && (this.id_ !== '')) {
        document.getElementsByClassName('goodButton')[0].click()
      }
      if ((e.keyCode === 50 || e.keyCode === 98) && (this.id_ !== '')) {
        document.getElementsByClassName('badButton')[0].click()
      }
      if ((e.keyCode === 51 || e.keyCode === 99) && (this.id_ !== '')) {
        document.getElementsByClassName('noValButton')[0].click()
      }
      if ((e.keyCode === 52 || e.keyCode === 100) && (this.id_ !== '')) {
        document.getElementsByClassName('nextButton')[0].click()
      }
    })
  }
}

function qualqueruma (e){
  console.log(e)
}
</script>

<style lang="scss" scoped>
  .News {
    display: flex;
    flex-direction: column;

    #UpperPart {
      display: flex;

      .title {
        display: flex;
        width: 100%;
        align-items: center;
        h1 {
          margin-left: 5%;
          text-align: left;
          width: 100%;
        }
      }

      .status {
        display: flex;
        flex-flow: column;
        width: 20%;
        align-items: center;
        justify-content: center;
        h3 {
          text-anchor: left;
          margin-right: 25%

        }
        p {
          text-anchor: left;
          margin-right: 25%
        }
      }

      
      .selectPanel {
        display: flex;
        flex-direction: column;
        height: 200px;
        width: 30%;
        margin-right: 5%;
        justify-content: flex-start;
        button {
          height: 25%;
          width: 100%;
        }
      }
    }

    #SubtitlePart{
      display: flex;
      justify-content: start;
      h2 {
        margin-top: 3%;
        margin-left: 5%;
        text-align: left;
      }
    }

    #Date{
      display: flex;
      justify-content: start;
      p {
        margin-left: 3%;
      }
      a {
        margin-left: 5%;
        margin-top: 15px;
        font-size: 15px;
      }
    }

    #Article{
      margin-left: 2%;
      margin-right: 3%;
      text-align: left;
      font-size: 20px;

    }
  }
</style>

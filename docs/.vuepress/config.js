module.exports = {
  head: [

    ['link', {
      rel: "stylesheet",
      href: "https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900|Material+Icons"
    }],
    ['link', {
      rel: "stylesheet",
      href: "https://cdn.jsdelivr.net/npm/vuetify/dist/vuetify.min.css"
    }],
  ],



  themeConfig: {
    repo: 'DavidCouronne/latexconvertmd',
    docsDir: 'docs',
    editLinks: true,
    editLinkText: 'Edit this page on GitHub',

    locales: {
      '/': {
        label: 'Français',
        selectText: 'Languages',
        lastUpdated: 'Last Updated'
      }
    },
    sidebarDepth: 3,
    nav: [{
        text: 'Accueil',
        link: '/'
      },
      {
        text: 'Guide',
        link: '/guide/'
      },
      {
        text: 'Katex',
        link: '/katex/'
      },
    ],
    sidebar: {
      '/docs/maths/sujets/2018-nvellecaledonie/': [
        '',
        'corrige',
      ],
      '/docs/informatique/Vuepress/': [
        '',
        'demarrer',
        'config1',
        'config2',
        'sidebar',
        'exercice',
        'katex',
        'deploy',

      ],
      '/docs/informatique/HowTo/': [
        ''
      ],
      '/docs/': [
        '',
      ],
    },

  },

  markdown: {
    lineNumbers: false,
    config: md => {
      md.use(require('./param-katex'));
    }
  }
}


module.exports = {
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
    extendMarkdown: md => {
      md.set({ breaks: true })
      md.use(require('markdown-it-katex-newcommand'))
    }
  }
}
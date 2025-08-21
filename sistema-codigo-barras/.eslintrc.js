module.exports = {
  root: true,
  env: {
    node: true,
    browser: true // Adicionado para ambiente de navegador
  },
  extends: [
    'plugin:vue/vue3-essential',
    'eslint:recommended'
  ],
  parserOptions: {
    parser: '@babel/eslint-parser'
  },
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off'
  },
  globals: {
    process: true // Informa ao ESLint que 'process' é uma variável global
  }
}

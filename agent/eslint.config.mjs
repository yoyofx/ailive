"use strict";

import globals from "globals";
import pluginJs from "@eslint/js";
import tseslint from "typescript-eslint";
import typescriptParser from "@typescript-eslint/parser"
import eslintCheckVarHttp from "./eslint-check.js";


export default  [
  ...tseslint.configs.stylistic,
  {
    files: ["**/*.{js,ts,jsx,tsx,vue}"],
    ignores: ["dist/**/*.cjs", "node_modules/**/*", "scripts/**/*"],
    languageOptions: {
      parser: typescriptParser,
      parserOptions: {
          requireConfigFile: false,
          babelOptions: {
              babelrc: false,
              configFile: false,
          }
      }
    },
    plugins: { "var-check-http-scheme": { rules: { "check-scheme": eslintCheckVarHttp } }, },
    rules: {
      "var-check-http-scheme/check-scheme": "error",
      "no-unused-expressions": "off",
      "@typescript-eslint/no-unused-vars": "off",
      '@typescript-eslint/recommended': 'off',
      "@typescript-eslint/consistent-type-definitions": "off",
      "@typescript-eslint/prefer-for-of": "off",
      "@typescript-eslint/no-empty-function": "off",
      "@typescript-eslint/adjacent-overload-signatures": "off",
      "semi": "off",
      "no-unused-vars": "off",
      "prefer-const": "off"
    }
  },
  // ...tseslint.configs.recommended,  
]
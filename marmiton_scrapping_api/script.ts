import { searchRecipes, MarmitonQueryBuilder, RECIPE_PRICE, RECIPE_DIFFICULTY } from 'marmiton-api'
import type { Recipe } from 'marmiton-api'
import { writeFile } from 'fs/promises'
const qb = new MarmitonQueryBuilder();
// A query builder is provided to make complex queries
const query = qb
  .withTitleContaining('soja')
  //.withoutOven()
  //.withPrice(RECIPE_PRICE.CHEAP)
  //.takingLessThan(45)
  //.withDifficulty(RECIPE_DIFFICULTY.EASY)
  .build()


// Fetch the recipes
const recipes: Recipe[] = await searchRecipes(query)
console.log(JSON.stringify(recipes, null, 2)) // pretty print


// async function main() {
//   const recipes: Recipe[] = await searchRecipes(query)

//   await writeFile(
//     'recipes.json',
//     JSON.stringify(recipes, null, 2), // pretty print
//     'utf-8'
//   )

//   console.log('Recipes saved to recipes.json')
// }

// main()

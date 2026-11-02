import { Element } from './element.js';

export class GameField {
    constructor(level, initialElementsConfig, rawRecipes) {
        this.level = level;
        this.elements = initialElementsConfig.map(item => new Element(item.type, item.x, item.y));

        // Превращаем рецепты в нормализованный словарь с отсортированными ключами
        this.recipes = {};
        for (const [key, result] of Object.entries(rawRecipes)) {
            const sortedKey = key.split('+').sort().join('+');
            this.recipes[sortedKey] = result;
        }
    }

    tryCraft(elem1, elem2) {
        const key = [elem1.typeId, elem2.typeId].sort().join('+');
        const resultType = this.recipes[key];

        if (resultType) {
            const newX = Math.floor((elem1.rect.x + elem2.rect.x) / 2);
            const newY = Math.floor((elem1.rect.y + elem2.rect.y) / 2);
            return new Element(resultType, newX, newY);
        }
        return null;
    }
}
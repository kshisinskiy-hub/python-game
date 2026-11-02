// selftest.js
import { Rect } from './js/rect.js';
import { Element } from './js/element.js';
import { STATE } from './js/constants.js';
import { DataManager } from './js/data_manager.js';
import { GameField } from './js/game_field.js';
import path from 'path';

let passedTests = 0;
let totalTests = 0;

function assert(condition, description) {
    totalTests++;
    if (condition) {
        passedTests++;
        console.log(`[PASS] ${description}`);
    } else {
        console.error(`[FAIL] ${description}`);
    }
}

console.log("=== ЗАПУСК САМОПРОВЕРКИ ЯДРА (LR 4) ===");

// Блок 1: Тесты геометрии и класса Rect (Тесты 1–6)
const r1 = new Rect(0, 0, 50, 50);
assert(r1.centerx === 25, "Тест 1: Расчет centerx для Rect");
assert(r1.centery === 25, "Тест 2: Расчет centery для Rect");

const r2 = r1.move(10, 20);
assert(r1.x === 0 && r1.y === 0, "Тест 3: Rect.move() возвращает копию, оригинал не мутирует");
assert(r2.x === 10 && r2.y === 20, "Тест 4: Координаты смещенного Rect корректны");

const r3 = new Rect(30, 30, 50, 50);
assert(r1.colliderect(r3) === true, "Тест 5: Обнаружение пересечения прямоугольников (colliderect)");
assert(r1.collidepoint(25, 25) === true, "Тест 6: Проверка попадания точки внутрь Rect (collidepoint)");

// Блок 2: Тесты математики и формул затухания (Тесты 7–10)
const e1 = new Element("fire", 0, 0);
const e2 = new Element("water", 30, 40); // расстояние = 50
assert(e1.distanceTo(e2) === 50, "Тест 7: Корректный расчет расстояния через Math.hypot");

const value0 = 1.0;
const decay = 0.02;
const d = 50;
const expectedValue = value0 * Math.exp(-decay * d); // ~0.3678
const calculatedValue = 1.0 * Math.exp(-0.02 * e1.distanceTo(e2));
assert(Math.abs(calculatedValue - expectedValue) < 0.0001, "Тест 8: Расчет экспоненциального затухания величины");

const thresholdPass = e1.checkThreshold(e2, 0.3, 0.02);
assert(thresholdPass === true, "Тест 9: Пороговое условие срабатывает, когда значение выше порога");

const thresholdFail = e1.checkThreshold(e2, 0.5, 0.02);
assert(thresholdFail === false, "Тест 10: Пороговое условие блокирует реакцию, если значение ниже порога");

// Блок 3: Тесты конечного автомата (Тесты 11–14)
const eStateTest = new Element("earth", 100, 100);
assert(eStateTest.state === STATE.IDLE, "Тест 11: Начальное состояние сущности — IDLE");

eStateTest.transitionTo(STATE.DRAGGING);
assert(eStateTest.state === STATE.DRAGGING, "Тест 12: Переход в состояние DRAGGING успешен");

eStateTest.transitionTo(STATE.CRAFTED);
assert(eStateTest.state === STATE.CRAFTED, "Тест 13: Переход в состояние CRAFTED успешен");

assert(STATE.IDLE !== STATE.DRAGGING && STATE.DRAGGING !== STATE.CRAFTED, "Тест 14: Состояния конечного автомата уникальны");

// Блок 4: Тесты загрузки JSON и валидации (Тесты 15–18)
const configPath = path.resolve("recipes.json");
const config = DataManager.loadConfig(configPath);
assert(config !== null && typeof config === 'object', "Тест 15: Успешная загрузка JSON-конфигурации");
assert(Array.isArray(config.initial_elements), "Тест 16: Валидация наличия initial_elements в конфиге");
assert(typeof config.recipes === 'object', "Тест 17: Валидация наличия recipes в конфиге");

let validationFailed = false;
try {
    DataManager._validate({ invalid_field: true });
} catch (e) {
    validationFailed = true;
}
assert(validationFailed === true, "Тест 18: Валидация отсеивает некорректную структуру конфигурации");

// Блок 5: Тесты игрового поля и логики крафта (Тесты 19–21)
const field = new GameField(config.level, config.initial_elements, config.recipes);
assert(field.elements.length === 4, "Тест 19: Игровое поле инициализирует стартовые элементы");

const fireElem = field.elements.find(el => el.typeId === "fire");
const waterElem = field.elements.find(el => el.typeId === "water");
const earthElem = field.elements.find(el => el.typeId === "earth");

const craftedSteam = field.tryCraft(fireElem, waterElem);
assert(craftedSteam !== null && craftedSteam.typeId === "steam", "Тест 20: Успешный крафт рецепта (fire + water = steam)");

const craftedLava = field.tryCraft(earthElem, fireElem);
assert(craftedLava !== null && craftedLava.typeId === "lava", "Тест 21: Порядок элементов не влияет на крафт благодаря сортировке ключей");

console.log(`\n=== ИТОГИ САМОПРОВЕРКИ ===`);
console.log(`Пройдено тестов: ${passedTests} из ${totalTests}`);

if (passedTests === totalTests) {
    console.log("ВСЕ ТЕСТЫ УСПЕШНО ПРОЙДЕНЫ!");
    process.exit(0);
} else {
    console.error("ОШИБКА: Некоторые тесты провалились.");
    process.exit(1);
}
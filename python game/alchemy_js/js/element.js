import { Rect } from './rect.js';
import { ELEMENT_DATA, STATE } from './constants.js';

export class Element {
    constructor(typeId, x, y, width = 80, height = 80) {
        this.typeId = typeId;
        this.name = ELEMENT_DATA[typeId] ? ELEMENT_DATA[typeId].name : typeId;
        this.rect = new Rect(x, y, width, height);
        this.state = STATE.IDLE;
        this.lastActionTime = 0;
    }

    // Метод конечного автомата для смены состояний
    transitionTo(newState) {
        this.state = newState;
    }

    // Расчет расстояния до другого элемента через Math.hypot
    distanceTo(other) {
        return Math.hypot(this.rect.centerx - other.rect.centerx, this.rect.centery - other.rect.centery);
    }

    // Проверка порогового условия срабатывания (экспоненциальное затухание по методичке)
    checkThreshold(other, threshold = 0.15, decayCoeff = 0.02, value0 = 1.0) {
        const d = this.distanceTo(other);
        const value = value0 * Math.exp(-decayCoeff * d);
        return value >= threshold;
    }
}
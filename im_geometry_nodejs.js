const distance = (x1, y1, x2, y2) => {
    return Math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2);
};

const midpoint = (x1, y1, x2, y2) => {
    const mx = (x1 + x2) / 2;
    const my = (y1 + y2) / 2;
    return [mx, my];
};

const getSlope = (x1, y1, x2, y2) => {
    if (x1 === x2) {
        x1 = x2 + 1;
        y2 = y1;
    }
    return (y2 - y1) / (x2 - x1);
};

const getAngle = (m1, m2) => {
    const tanTheta = (m1 - m2) / (1 + m1 * m2);
    let thetaDegrees = Math.atan(tanTheta) * (180 / Math.PI);
    
    if (thetaDegrees < 0) {
        thetaDegrees += 180;
    }
    
    return thetaDegrees;
};

module.exports = {
    distance,
    midpoint,
    getSlope,
    getAngle
};
// Assuming getAngle and getSlope are imported from a separate file
const { getAngle, getSlope } = require('./im_geometry_nodejs');

function getFace(plList) {
    return {
        l_eye: [Math.floor(plList[2].x), Math.floor(plList[2].y)],
        r_eye: [Math.floor(plList[5].x), Math.floor(plList[5].y)],
        nose: [Math.floor(plList[0].x), Math.floor(plList[0].y)],
        l_ear: [Math.floor(plList[7].x), Math.floor(plList[7].y)],
        r_ear: [Math.floor(plList[8].x), Math.floor(plList[8].y)],
        l_mouth: [Math.floor(plList[9].x), Math.floor(plList[9].y)],
        r_mouth: [Math.floor(plList[10].x), Math.floor(plList[10].y)]
    };
}

function getLeftArm(plList) {
    const lshSlope = getSlope(plList[11].x, plList[11].y, plList[23].x, plList[23].y);
    const lseSlope = getSlope(plList[11].x, plList[11].y, plList[13].x, plList[13].y);
    const lewSlope = getSlope(plList[13].x, plList[13].y, plList[15].x, plList[15].y);

    const hsSeAngle = getAngle(lshSlope, lseSlope);
    const seEwAngle = getAngle(lseSlope, lewSlope);

    const hssea = Math.floor(hsSeAngle);
    const seewa = 180 - Math.floor(seEwAngle);

    return {
        shoulder: [Math.floor(plList[11].x), Math.floor(plList[11].y)],
        elbow: [Math.floor(plList[13].x), Math.floor(plList[13].y)],
        wrist: [Math.floor(plList[15].x), Math.floor(plList[15].y)],
        index: [Math.floor(plList[19].x), Math.floor(plList[19].y)],
        arm_body_angle: hssea,
        elbow_angle: seewa
    };
}

function getLeftLeg(plList) {
    const lhkSlope = getSlope(plList[23].x, plList[23].y, plList[25].x, plList[25].y);
    const lkaSlope = getSlope(plList[25].x, plList[25].y, plList[27].x, plList[27].y);

    const hkKaAngle = getAngle(lhkSlope, lkaSlope);
    const hkkaa = Math.floor(hkKaAngle);

    return {
        hip: [Math.floor(plList[23].x), Math.floor(plList[23].y)],
        knee: [Math.floor(plList[25].x), Math.floor(plList[25].y)],
        ankle: [Math.floor(plList[27].x), Math.floor(plList[27].y)],
        heel: [Math.floor(plList[29].x), Math.floor(plList[29].y)],
        toes: [Math.floor(plList[31].x), Math.floor(plList[31].y)],
        knee_angle: hkkaa
    };
}

function getRightArm(plList) {
    const rshSlope = getSlope(plList[12].x, plList[12].y, plList[24].x, plList[24].y);
    const rseSlope = getSlope(plList[12].x, plList[12].y, plList[14].x, plList[14].y);
    const rewSlope = getSlope(plList[14].x, plList[14].y, plList[16].x, plList[16].y);

    const hsSeAngle = getAngle(rshSlope, rseSlope);
    const seEwAngle = getAngle(rseSlope, rewSlope);

    const hssea = 180 - Math.floor(hsSeAngle);
    const seewa = Math.floor(seEwAngle);

    return {
        shoulder: [Math.floor(plList[12].x), Math.floor(plList[12].y)],
        elbow: [Math.floor(plList[14].x), Math.floor(plList[14].y)],
        wrist: [Math.floor(plList[16].x), Math.floor(plList[16].y)],
        index: [Math.floor(plList[20].x), Math.floor(plList[20].y)],
        arm_body_angle: hssea,
        elbow_angle: seewa
    };
}

function getRightLeg(plList) {
    const rhkSlope = getSlope(plList[24].x, plList[24].y, plList[26].x, plList[26].y);
    const rkaSlope = getSlope(plList[26].x, plList[26].y, plList[28].x, plList[28].y);

    const hkKaAngle = getAngle(rhkSlope, rkaSlope);
    const hkkaa = 180 - Math.floor(hkKaAngle);

    return {
        hip: [Math.floor(plList[24].x), Math.floor(plList[24].y)],
        knee: [Math.floor(plList[26].x), Math.floor(plList[26].y)],
        ankle: [Math.floor(plList[28].x), Math.floor(plList[28].y)],
        heel: [Math.floor(plList[30].x), Math.floor(plList[30].y)],
        toes: [Math.floor(plList[32].x), Math.floor(plList[32].y)],
        knee_angle: hkkaa
    };
}

module.exports = {
    getFace,
    getLeftArm,
    getLeftLeg,
    getRightArm,
    getRightLeg
};
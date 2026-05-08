// script.js

let attendanceCounter = 0;
let equipmentCounter = 0;

// Attendance
function addAttendance(){

    let name = document.getElementById("cadetName").value;
    let rank = document.getElementById("rank").value;
    let platoon = document.getElementById("platoon").value;
    let status = document.getElementById("status").value;
    let date = document.getElementById("attendanceDate").value;

    if(name === "" || rank === "" || platoon === "" || status === "" || date === ""){
        alert("Please complete all attendance fields.");
        return;
    }

    let table = document.getElementById("attendanceTable");

    let row = `
        <tr>
            <td>${name}</td>
            <td>${rank}</td>
            <td>${platoon}</td>
            <td>${status}</td>
            <td>${date}</td>
        </tr>
    `;

    table.innerHTML += row;

    attendanceCounter++;

    document.getElementById("attendanceCount").innerText = attendanceCounter;

    document.getElementById("cadetName").value = "";
    document.getElementById("rank").value = "";
    document.getElementById("platoon").value = "";
    document.getElementById("status").value = "";
    document.getElementById("attendanceDate").value = "";
}

// Equipment
function addEquipment(){

    let borrower = document.getElementById("borrowerName").value;
    let equipment = document.getElementById("equipment").value;
    let quantity = document.getElementById("quantity").value;
    let date = document.getElementById("borrowDate").value;

    if(borrower === "" || equipment === "" || quantity === "" || date === ""){
        alert("Please complete all equipment fields.");
        return;
    }

    let table = document.getElementById("equipmentTable");

    let row = `
        <tr>
            <td>${borrower}</td>
            <td>${equipment}</td>
            <td>${quantity}</td>
            <td>${date}</td>
        </tr>
    `;

    table.innerHTML += row;

    equipmentCounter += parseInt(quantity);

    document.getElementById("equipmentCount").innerText = equipmentCounter;

    document.getElementById("borrowerName").value = "";
    document.getElementById("equipment").value = "";
    document.getElementById("quantity").value = "";
    document.getElementById("borrowDate").value = "";
}
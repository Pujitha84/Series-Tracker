// ===============================
// ADD SERIES FORM
// ===============================

function openForm() {

    const form = document.getElementById("formBox");

    if (form.style.display === "block") {

        form.style.display = "none";

    } else {

        form.style.display = "block";

        form.scrollIntoView({
            behavior: "smooth",
            block: "center"
        });
    }
}


// ===============================
// EDIT SERIES FORM
// ===============================

function openEditForm(id) {

    const form = document.getElementById("editForm" + id);

    if (form) {

        form.style.display = "block";

        form.scrollIntoView({
            behavior: "smooth",
            block: "center"
        });

    }
}


function closeEditForm(id) {

    const form = document.getElementById("editForm" + id);

    if (form) {

        form.style.display = "none";

    }
}


// ===============================
// EDIT BUTTONS
// ===============================

document.querySelectorAll(".edit-btn").forEach(button => {

    button.addEventListener("click", function () {

        const id = this.dataset.id;

        openEditForm(id);

    });

});


// ===============================
// CANCEL BUTTONS
// ===============================

document.querySelectorAll(".cancel-btn").forEach(button => {

    button.addEventListener("click", function () {

        const id = this.dataset.cancelId;

        closeEditForm(id);

    });

});


// ===============================
// PROGRESS BARS
// ===============================

document.querySelectorAll(".progress-bar").forEach(bar => {

    const watched = Number(bar.dataset.watched);
    const total = Number(bar.dataset.total);

    let percentage = 0;

    if (total > 0) {

        percentage = (watched / total) * 100;

    }

    if (percentage > 100) {

        percentage = 100;

    }

    if (percentage < 0) {

        percentage = 0;

    }

    bar.style.width = percentage + "%";

});
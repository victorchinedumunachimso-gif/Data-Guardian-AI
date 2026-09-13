// ========================================
// Data Guardian AI
// Upload & Analyze Dataset
// ========================================

console.log("✅ upload.js loaded");


// ========================================
// GET HTML ELEMENTS
// ========================================

const uploadForm =
    document.getElementById("uploadForm");

const fileInput =
    document.getElementById("dataset");

const promptInput =
    document.getElementById("prompt");

const loading =
    document.getElementById("loading");

const result =
    document.getElementById("result");

const fileInfo =
    document.getElementById("fileInfo");

const fileName =
    document.getElementById("fileName");

const dropZone =
    document.getElementById("dropZone");


// ========================================
// CHECK FORM
// ========================================

if (!uploadForm) {

    console.error(
        "❌ uploadForm was not found."
    );

}


// ========================================
// FILE SELECTION
// ========================================

if (fileInput) {

    fileInput.addEventListener(
        "change",
        function () {

            if (
                fileInput.files &&
                fileInput.files.length > 0
            ) {

                const file =
                    fileInput.files[0];

                if (fileName) {

                    fileName.textContent =
                        file.name;

                }

                if (fileInfo) {

                    fileInfo.classList.add(
                        "show"
                    );

                }

                console.log(
                    "📁 File selected:",
                    file.name
                );

            }

        }
    );

}


// ========================================
// DRAG OVER
// ========================================

if (dropZone) {

    dropZone.addEventListener(
        "dragover",
        function (e) {

            e.preventDefault();

            dropZone.classList.add(
                "dragging"
            );

        }
    );


    // ========================================
    // DRAG LEAVE
    // ========================================

    dropZone.addEventListener(
        "dragleave",
        function () {

            dropZone.classList.remove(
                "dragging"
            );

        }
    );


    // ========================================
    // DROP
    // ========================================

    dropZone.addEventListener(
        "drop",
        function (e) {

            e.preventDefault();

            dropZone.classList.remove(
                "dragging"
            );

            const files =
                e.dataTransfer.files;

            if (
                files &&
                files.length > 0
            ) {

                const file =
                    files[0];

                try {

                    const dataTransfer =
                        new DataTransfer();

                    dataTransfer.items.add(
                        file
                    );

                    fileInput.files =
                        dataTransfer.files;

                }

                catch (error) {

                    console.error(
                        "❌ Could not attach dropped file:",
                        error
                    );

                }


                if (fileName) {

                    fileName.textContent =
                        file.name;

                }

                if (fileInfo) {

                    fileInfo.classList.add(
                        "show"
                    );

                }

                console.log(
                    "📁 File dropped:",
                    file.name
                );

            }

        }
    );

}


// ========================================
// UPLOAD FORM
// ========================================

if (uploadForm) {

    uploadForm.addEventListener(
        "submit",
        async function (e) {

            e.preventDefault();

            console.log(
                "🚀 Analyze button clicked"
            );


            // --------------------------------
            // Clear result
            // --------------------------------

            if (result) {

                result.innerHTML = "";

            }


            // --------------------------------
            // Show loading
            // --------------------------------

            if (loading) {

                loading.style.display =
                    "block";

            }


            // --------------------------------
            // Check file
            // --------------------------------

            if (
                !fileInput ||
                !fileInput.files ||
                fileInput.files.length === 0
            ) {

                alert(
                    "Please choose a dataset."
                );

                if (loading) {

                    loading.style.display =
                        "none";

                }

                return;

            }


            // --------------------------------
            // Create FormData
            // --------------------------------

            const formData =
                new FormData();

            formData.append(
                "file",
                fileInput.files[0]
            );

            formData.append(
                "prompt",
                promptInput
                    ? promptInput.value
                    : ""
            );


            try {

                console.log(
                    "📤 Sending dataset to backend..."
                );


                // ========================================
                // FASTAPI REQUEST
                // ========================================

                const response =
                    await fetch(
                        "http://127.0.0.1:8000/api/v1/analyze",
                        {
                            method: "POST",
                            body: formData
                        }
                    );


                console.log(
                    "📡 Backend status:",
                    response.status
                );


                // ========================================
                // READ RESPONSE
                // ========================================

                const data =
                    await response.json();


                console.log(
                    "✅ Backend Response:",
                    data
                );


                if (loading) {

                    loading.style.display =
                        "none";

                }


                // ========================================
                // BACKEND ERROR
                // ========================================

                if (!response.ok) {

                    if (result) {

                        result.innerHTML = `

                            <h2 style="color:red;">
                                ❌ Backend Error
                            </h2>

                            <pre>${JSON.stringify(
                                data,
                                null,
                                4
                            )}</pre>

                        `;

                    }

                    return;

                }


                // ========================================
                // SAVE RESULT
                // ========================================

                localStorage.setItem(
                    "analysisResult",
                    JSON.stringify(data)
                );


                console.log(
                    "💾 Analysis saved successfully"
                );


                // ========================================
                // VERIFY SAVE
                // ========================================

                const saved =
                    localStorage.getItem(
                        "analysisResult"
                    );

                console.log(
                    "💾 Saved result:",
                    saved
                );


                // ========================================
                // SUCCESS MESSAGE
                // ========================================

                if (result) {

                    result.innerHTML = `

                        <div class="success-message">

                            <h2>
                                ✅ Analysis Completed
                            </h2>

                            <p>
                                Your dataset has been analyzed successfully.
                            </p>

                            <p>
                                Redirecting to dashboard...
                            </p>

                        </div>

                    `;

                }


                // ========================================
                // REDIRECT
                // ========================================

                setTimeout(
                    function () {

                        window.location.href =
                            "dashboard.html";

                    },
                    1000
                );

            }


            catch (error) {

                if (loading) {

                    loading.style.display =
                        "none";

                }


                console.error(
                    "❌ JavaScript Error:",
                    error
                );


                if (result) {

                    result.innerHTML = `

                        <h2 style="color:red;">
                            ❌ Connection / JavaScript Error
                        </h2>

                        <pre>${error.message}</pre>

                    `;

                }

            }

        }
    );

}
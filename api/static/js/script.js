// childcare/api/static/js/script.js
document.addEventListener("DOMContentLoaded", function() {
    fetchChildren();
});

function fetchChildren() {
    fetch("{% url 'get_children' %}")  // AJAX request to fetch children data
        .then(response => response.json())
        .then(data => {
            if (data.children) {
                let childList = document.getElementById("child-list");
                childList.innerHTML = "";  // Clear previous data

                data.children.forEach(child => {
                    let listItem = document.createElement("li");
                    listItem.textContent = `${child.name} (Age: ${child.age})`;
                    childList.appendChild(listItem);
                });
            }
        })
        .catch(error => console.error("Error fetching children:", error));
}

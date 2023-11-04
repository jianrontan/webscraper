function sortTable(n, desc = false) {
    let table, rows, switching, i, x, y, shouldSwitch;
    table = document.querySelector(".products_table table");
    switching = true;

    while (switching) {
        switching = false;
        rows = table.rows;
        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            x = rows[i].getElementsByTagName("td")[n];
            y = rows[i + 1].getElementsByTagName("td")[n];

            if (!desc && Number(x.innerHTML) > Number(y.innerHTML) || desc && Number(x.innerHTML) < Number(y.innerHTML)) {
                shouldSwitch = true;
                break;
            }
        }
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
        }
    }
    for (i = 1; i < rows.length; i ++) {
        rows[i].cells[0].innerHTML = i;
    }
}
function priceSorting() {
    var priceHeader = document.getElementById("priceHeader");
    priceHeader.addEventListener("click", function(){
        if (sortOrder === 0) {
            sortTable(2);
            sortOrder++;
        }
        else if (sortOrder === 1) {
            sortTable(2, true);
            sortOrder++;
        }
        else if (sortOrder === 2) {
            sortTable(2, false);
            sortOrder = 1;
            // Can implement reset table in the future
        }
    });
}
window.onload = priceSorting;
function validateForm() {
    var query = document.getElementById("query").value;
    if (query === "sessions") {
        alert("Invalid query");
        return false;
    }
    return true;
};
function multipleEncode(encodee) {
    return encodeURIComponent(encodeURIComponent(encodee));
}
function getProductData(tableName, productName, productSeller) {
    fetch(`/product/${multipleEncode(tableName)}/${multipleEncode(productName)}/${multipleEncode(productSeller)}`)
        .then(response => response.json())
        .then(data => {
            // Create the product_data table
            let table1 = `<h3>Historical Product Data</h3><table class="products_table"><thead><tr><th class="alignment border">Index</th><th class="alignment border">Product</th><th class="alignment border">Price</th><th class="alignment border">Seller</th><th class="alignment border">Link</th><th class="alignment border">Date Scraped</th></tr></thead><tbody>`;
            let index = 1;
            data.product_data.forEach(row => {
                table1 += "<tr>";
                table1 += `<td class="alignment border">${index++}</td>`
                for (let i = 1; i < row.length; i++) {
                    if (i === 4) {
                        table1 += `<td class="alignment border"><a href="${row[i]}">Link</a></td>`;
                    } else {
                        table1 += `<td class="alignment border">${row[i]}</td>`;
                    }
                }
                table1 += "</tr>";
            });
            table1 += "</tbody></table>";
            // Create the other_product_data table if it's not empty
            let table2 = "";
            if (data.other_product_data.length > 0) {
                table2 = `<h3>Seller Other Product Data</h3><table class="products_table"><thead><tr><th class="alignment border">Index</th><th class="alignment border">Product</th><th class="alignment border">Price</th><th class="alignment border">Seller</th><th class="alignment border">Link</th><th class="alignment border">Date Scraped</th></tr></thead><tbody>`;
                index = 1;
                data.other_product_data.forEach(row => {
                    table2 += "<tr>";
                    table2 += `<td class="alignment border">${index++}</td>`;
                    for (let i = 1; i < row.length; i++) {
                        if (i === 4) {
                            table2 += `<td class="alignment border"><a href="${row[i]}">Link</a></td>`;
                        } else {
                            table2 += `<td class="alignment border">${row[i]}</td>`;
                        }
                    }
                    table2 += "</tr>";
                });
                table2 += "</tbody></table>";
            }
            document.getElementById("productData").innerHTML = table1 + table2;
            modal.style.display = "block";
            document.getElementById('overlay').style.display = "block";
        })
        .catch(error => console.error('Error:', error));
};
var modal = document.getElementById("productModal");
var span = document.getElementsByClassName("close")[0];
var overlay = document.getElementById('overlay');
var modalContent = document.querySelector(".modalContent");
var sortOrder = 0;
// When the user clicks on <span> (the X), close the modal
span.onclick = function() {
    modal.style.display = "none";
    document.getElementById('overlay').style.display = "none";
    document.body.style.pointerEvents = "auto";
};
// When the user clicks on the overlay, close the modal
overlay.onclick = function() {
    modal.style.display = "none";
    overlay.style.display = "none";
    document.body.style.pointerEvents = "auto";
};
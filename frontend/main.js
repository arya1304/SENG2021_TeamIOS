// register
document.getElementById('btn-register').addEventListener('click', async () => {
    const username = document.getElementById('register-name').value;
    const password = document.getElementById('register-password').value;
    
    try {
        const response = await fetch("https://t6r6w5zni9.execute-api.us-east-1.amazonaws.com/v3/users/signUp", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
        });

        if (!response.ok) {
            alert('Failed to register')
        }

        const data = await response.json();
        console.log("register response:", data);

        showPage("main")
    } catch (err) {
        console.error(err.message);
    }
});

// login
document.getElementById('btn-login').addEventListener('click', async () => {
    const username = document.getElementById('login-name').value;
    const password = document.getElementById('login-password').value;
    
    try {
        const response = await fetch("https://t6r6w5zni9.execute-api.us-east-1.amazonaws.com/v3/users/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
        });

        if (!response.ok) {
            alert('Failed to login')
        }

        const data = await response.json();
        console.log("login response:", data);

        sessionStorage.setItem("token", data.token);
        showPage("main")
    } catch (err) {
        console.error(err.message);
    }
});

document.getElementById('btn-list-advice').addEventListener('click', async () => {    
    try {
        const token = sessionStorage.getItem("token");

        const response = await fetch("https://t6r6w5zni9.execute-api.us-east-1.amazonaws.com/v3/despatchAdvice", {
        method: "GET",
        headers: {
            Authorization: token
        }
        });

        if (!response.ok) {
            alert('Failed to get lists')
        }

        const data = await response.json();
        console.log(data.despatchAdvicesIDs);
        console.log("get list advices response:", data);

        const listContainer = document.getElementById("despatch-list");
        listContainer.innerHTML = "";

        const ids = data.despatchAdvices.despatchAdvicesIDs;

        ids.forEach((idText) => {
            const li = document.createElement("li");
            li.textContent = idText;
            listContainer.appendChild(li);
        });


        showPage("main")
    } catch (err) {
        console.error(err.message);
    }
});

document.getElementById('btn-get-user').addEventListener('click', async() => {
    const id = document.getElementById('user-id').value;

    try {
        const token = sessionStorage.getItem("token");

        const response = await fetch(`https://seapi.vercel.app/v1/user/${id}`, {
            method: "GET",
            headers: {
                Authorization: `Bearer ${token}`
            }
    });

        if (!response.ok) {
            alert('Failed to get user')
        }

        const data = await response.json();
        console.log("user response:", data);

        showPage("main")
    } catch (err) {
        console.error(err.message);
    }
})

document.getElementById('btn-delete-advice').addEventListener('click', async() => {
    const despatchId = document.getElementById('delete-id').value;

    try {
        const token = sessionStorage.getItem("token");

        const response = await fetch(`https://t6r6w5zni9.execute-api.us-east-1.amazonaws.com/v1/despatchAdvice/${despatchId}`, {
            method: "DELETE",
            headers: {
                Authorization: `Bearer ${token}`
            }
    });

        if (!response.ok) {
            alert('Failed to delete')
        }

        const data = await response.json();
        console.log("user response:", data);

        showPage("main")
    } catch (err) {
        console.error(err.message);
    }
})

document.getElementById('btn-delete-user').addEventListener('click', async() => {
    const id = document.getElementById('user-id').value;

    try {
        const token = sessionStorage.getItem("token");

        const response = await fetch(`https://seapi.vercel.app/v1/user/${id}`, {
            method: "DELETE",
            headers: {
                Authorization: `Bearer ${token}`
            }
    });

        if (!response.ok) {
            alert('Failed to delete user')
        }

        const data = await response.json();
        console.log("user response:", data);

        showPage("main")
    } catch (err) {
        console.error(err.message);
    }
})

// document.getElementById('btn-create-order').addEventListener('click', async () => {
//     const id = document.getElementById('order-id').value;
//     const date = document.getElementById('issue-date').value;
//     const currency = document.getElementById('currency-select').value;
//     const name = document.getElementById('buyer-name').value;
//     const email = document.getElementById('buyer-email').value;
//     const totalAmount = document.getElementById('total-amount').value;

//     const orderPayload = {
//         "_D": "urn:oasis:names:specification:ubl:schema:xsd:Order-2",
//         "_S": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
//         "_B": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
//         "Order": [
//             {
//                 "UBLVersionID": [
//                     {
//                         "IdentifierContent": "1",
//                         "IdentificationSchemeAgencyIdentifier": "1",
//                         "IdentificationSchemeIdentifier": "1"
//                     }
//                 ],
//                 "CustomizationID": [
//                     {
//                         "IdentifierContent": "1",
//                         "IdentificationSchemeAgencyIdentifier": "1",
//                         "IdentificationSchemeIdentifier": "1"
//                     }
//                 ],
//                 "ProfileID": [
//                     {
//                         "IdentifierContent": "1",
//                         "IdentificationSchemeAgencyIdentifier": "1",
//                         "IdentificationSchemeIdentifier": "1"
//                     }
//                 ],
//                 "ID": [
//                     {
//                         "IdentifierContent": id
//                     }
//                 ],
//                 "IssueDate": [
//                     {
//                         "DateContent": date
//                     }
//                 ],
//                 "DocumentCurrencyCode": [
//                     {
//                         "CodeContent": currency
//                     }
//                 ],
//                 "BuyerCustomerParty": [
//                     {
//                         "Party": [
//                             {
//                                 "PartyName": [
//                                     {
//                                         "Name": [
//                                             {
//                                                 "TextContent": name
//                                             }
//                                         ]
//                                     }
//                                 ],
//                                 "Contact": [
//                                     {
//                                         "ElectronicMail": [
//                                             {
//                                                 "TextContent": email
//                                             }
//                                         ]
//                                     }
//                                 ]
//                             }
//                         ]
//                     }
//                 ],
//                 "SellerSupplierParty": [
//                     {
//                         "Party": [
//                             {
//                                 "PartyName": [
//                                     {
//                                         "Name": [
//                                             {
//                                                 "TextContent": "supplier"
//                                             }
//                                         ]
//                                     }
//                                 ]
//                             }
//                         ]
//                     }
//                 ],
//                 "OrderLine": [
//                     {
//                         "Note": [
//                             {
//                                 "TextContent": "Test line item"
//                             }
//                         ],
//                         "LineItem": [
//                             {
//                                 "ID": [
//                                     {
//                                         "IdentifierContent": "1"
//                                     }
//                                 ],
//                                 "Quantity": [
//                                     {
//                                         "QuantityContent": 1,
//                                         "QuantityUnitCode": "EA"
//                                     }
//                                 ],
//                                 "LineExtensionAmount": [
//                                     {
//                                         "AmountContent": parseFloat(totalAmount),
//                                         "AmountCurrencyIdentifier": currency
//                                     }
//                                 ]
//                             }
//                         ]
//                     }
//                 ],
//                 "AnticipatedMonetaryTotal": [
//                     {
//                         "PayableAmount": [
//                             {
//                                 "AmountContent": parseFloat(totalAmount),
//                                 "AmountCurrencyIdentifier": currency
//                             }
//                         ]
//                     }
//                 ]
//             }
//         ]
//     };

//     try {
//         const token = sessionStorage.getItem("token");
//         const response = await fetch("https://seapi.vercel.app/v1/order", {
//         method: "POST",
//         headers: {
//             "Content-Type": "application/json",
//             Authorization: `Bearer ${token}`
//         },
//         body: JSON.stringify(orderPayload)
//         });

//         if (!response.ok) {
//             alert('Failed to create order')
//         }
//         const data = await response.json();
//         console.log("create order response:", data);

//     } catch (err) {
//         console.error(err.message);
//     }
// });



const callProtectedAPI = async () => {
    const token = localStorage.getItem("token");
  
    const res = await fetch("https://seapi.vercel.app/v1/some/protected/endpoint", {
        method: "GET",
        headers: {
        Authorization: `Bearer ${token}`
      }
    });
  
    const data = await res.json();
};

const showPage = (pageName) => {
    const pages = document.querySelectorAll('.page');
    for (const page of pages) {
        page.classList.add('hide');
    }
    document.getElementById(`page-${pageName}`).classList.remove('hide');
}

document.addEventListener("DOMContentLoaded", () => {
    showPage("landing");
});
document.getElementById('btn-register').addEventListener('click', async () => {
    const email = document.getElementById('register-email').value;
    const firstName = document.getElementById('register-first-name').value;
    const lastName = document.getElementById('register-last-name').value;
    const password = document.getElementById('register-password').value;
    
    try {
        const response = await fetch("https://seapi.vercel.app/v1/auth/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: email,
            first_name: firstName,
            last_name: lastName,
            password: password
        })
        });

        if (!response.ok) {
            alert('Failed to register')
        }

        const data = await response.json();
        console.log("register response:", data);

        sessionStorage.setItem("token", data.data.session.access_token);
        showPage("main")
    } catch (err) {
        console.error(err.message);
    }
});

document.getElementById('btn-login').addEventListener('click', async () => {
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    
    try {
        const response = await fetch("https://seapi.vercel.app/v1/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: email,
            password: password
        })
        });

        if (!response.ok) {
            alert('Failed to login')
        }

        const data = await response.json();
        console.log("login response:", data);

        sessionStorage.setItem("token", data.data.session.access_token);
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
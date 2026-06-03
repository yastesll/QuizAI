/* 
    Fichier : main.js
    Auteur : VIDZRAKOU
    Date : 04/06/2026
    But : logique JavaScript du projet QuizAI
*/

// Gère le toggle du thème (clair/sombre) s'il existe un bouton
const themeToggle = document.getElementById('themeToggle'); // on récupère le bouton de basculement du thème s'il existe
if (themeToggle) { // si le bouton existe
    themeToggle.addEventListener('click', function() { // on ajoute un écouteur d'événement au clic
        document.documentElement.setAttribute('data-theme', 
            document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'); // on bascule entre les thèmes clair et sombre
    });
}

// Fonction pour formater les dates
function formatDate(dateString) { // on définit une fonction pour formater les dates
    const date = new Date(dateString); // on crée une date à partir de la chaîne
    return date.toLocaleDateString('fr-FR', { // on formate la date en français
        year: 'numeric', // on affiche l'année
        month: 'long', // on affiche le mois
        day: 'numeric' // on affiche le jour
    });
}

// Fonction pour afficher les notifications
function showNotification(message, type = 'info') { // on définit une fonction pour afficher des notifications
    const notification = document.createElement('div'); // on crée un élément div
    notification.className = `notification notification-${type}`; // on ajoute les classes
    notification.textContent = message; // on ajoute le message
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem;
        background-color: ${type === 'error' ? '#d32f2f' : type === 'success' ? '#00c853' : '#1a237e'};
        color: white;
        border-radius: 5px;
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `; // on ajoute les styles
    document.body.appendChild(notification); // on ajoute la notification au body
    
    setTimeout(() => { // on définit un délai
        notification.remove(); // on supprime la notification après 3 secondes
    }, 3000);
}

// Gère les erreurs de requête fetch
async function fetchWithError(url, options = {}) { // on définit une fonction pour les requêtes fetch avec gestion d'erreur
    try { // on essaie d'exécuter le code
        const response = await fetch(url, options); // on envoie la requête
        if (!response.ok) { // si la réponse n'est pas correcte
            throw new Error(`HTTP error! status: ${response.status}`); // on lève une erreur
        }
        return await response.json(); // on retourne la réponse en JSON
    } catch (error) { // si une erreur survient
        showNotification('Une erreur est survenue. Veuillez réessayer.', 'error'); // on affiche une notification d'erreur
        console.error('Erreur:', error); // on affiche l'erreur dans la console
        return null; // on retourne null
    }
}

// Validation des formulaires
function validateEmail(email) { // on définit une fonction pour valider les emails
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // on crée une expression régulière
    return re.test(email); // on teste l'email
}

function validatePassword(password) { // on définit une fonction pour valider les mots de passe
    return password.length >= 6; // on vérifie que le mot de passe a au moins 6 caractères
}

// Gère les formulaires d'authentification
const loginForm = document.querySelector('form[action="/login"]'); // on récupère le formulaire de connexion s'il existe
if (loginForm) { // si le formulaire existe
    loginForm.addEventListener('submit', function(e) { // on ajoute un écouteur d'événement à la soumission
        const email = this.querySelector('input[name="email"]').value; // on récupère l'email
        const password = this.querySelector('input[name="mot_de_passe"]').value; // on récupère le mot de passe
        
        if (!validateEmail(email)) { // si l'email n'est pas valide
            e.preventDefault(); // on empêche la soumission
            showNotification('Veuillez entrer un email valide', 'error'); // on affiche une notification d'erreur
        }
    });
}

const registerForm = document.querySelector('form[action="/register"]'); // on récupère le formulaire d'inscription s'il existe
if (registerForm) { // si le formulaire existe
    registerForm.addEventListener('submit', function(e) { // on ajoute un écouteur d'événement à la soumission
        const email = this.querySelector('input[name="email"]').value; // on récupère l'email
        const password = this.querySelector('input[name="mot_de_passe"]').value; // on récupère le mot de passe
        const nom = this.querySelector('input[name="nom"]').value; // on récupère le nom
        
        if (!nom.trim()) { // si le nom est vide
            e.preventDefault(); // on empêche la soumission
            showNotification('Veuillez entrer votre nom', 'error'); // on affiche une notification d'erreur
        } else if (!validateEmail(email)) { // si l'email n'est pas valide
            e.preventDefault(); // on empêche la soumission
            showNotification('Veuillez entrer un email valide', 'error'); // on affiche une notification d'erreur
        } else if (!validatePassword(password)) { // si le mot de passe n'est pas valide
            e.preventDefault(); // on empêche la soumission
            showNotification('Le mot de passe doit contenir au moins 6 caractères', 'error'); // on affiche une notification d'erreur
        }
    });
}

// Gère l'upload de fichiers
const uploadForm = document.querySelector('form[action="/upload"]'); // on récupère le formulaire d'upload s'il existe
if (uploadForm) { // si le formulaire existe
    uploadForm.addEventListener('submit', function(e) { // on ajoute un écouteur d'événement à la soumission
        const titre = this.querySelector('input[name="titre"]').value; // on récupère le titre
        const fichier = this.querySelector('input[name="fichier"]').files[0]; // on récupère le fichier
        const texte = this.querySelector('textarea[name="texte"]').value; // on récupère le texte
        
        if (!titre.trim()) { // si le titre est vide
            e.preventDefault(); // on empêche la soumission
            showNotification('Veuillez entrer un titre', 'error'); // on affiche une notification d'erreur
        } else if (!fichier && !texte.trim()) { // si ni fichier ni texte ne sont fournis
            e.preventDefault(); // on empêche la soumission
            showNotification('Veuillez fournir un PDF ou du texte', 'error'); // on affiche une notification d'erreur
        } else if (fichier && !fichier.name.endsWith('.pdf')) { // si le fichier n'est pas un PDF
            e.preventDefault(); // on empêche la soumission
            showNotification('Seuls les fichiers PDF sont acceptés', 'error'); // on affiche une notification d'erreur
        } else if (fichier && fichier.size > 2097152) { // si le fichier est plus gros que 2 Mo
            e.preventDefault(); // on empêche la soumission
            showNotification('Le fichier doit faire moins de 2 Mo', 'error'); // on affiche une notification d'erreur
        }
    });
}

// Animation de chargement
function showLoadingSpinner() { // on définit une fonction pour afficher un spinner de chargement
    const spinner = document.createElement('div'); // on crée un élément div
    spinner.id = 'loadingSpinner'; // on définit l'id
    spinner.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 10001;
        width: 50px;
        height: 50px;
        border: 5px solid #f3f3f3;
        border-top: 5px solid #1a237e;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    `; // on ajoute les styles
    
    const style = document.createElement('style'); // on crée un élément style
    style.textContent = `
        @keyframes spin {
            0% { transform: translate(-50%, -50%) rotate(0deg); }
            100% { transform: translate(-50%, -50%) rotate(360deg); }
        }
    `; // on ajoute l'animation
    document.head.appendChild(style); // on ajoute le style au head
    document.body.appendChild(spinner); // on ajoute le spinner au body
}

function hideLoadingSpinner() { // on définit une fonction pour cacher le spinner
    const spinner = document.getElementById('loadingSpinner'); // on récupère le spinner
    if (spinner) { // si le spinner existe
        spinner.remove(); // on le supprime
    }
}

// Gère les clics en dehors des modals
window.addEventListener('click', function(event) { // on ajoute un écouteur d'événement au clic global
    const modals = document.querySelectorAll('.modal'); // on récupère tous les modals
    modals.forEach(modal => { // pour chaque modal
        if (event.target === modal) { // si le clic est en dehors du modal
            modal.style.display = 'none'; // on cache le modal
        }
    });
});

// Fonction utilitaire pour copier du texte
function copyToClipboard(text) { // on définit une fonction pour copier du texte
    navigator.clipboard.writeText(text).then(() => { // on copie le texte
        showNotification('Copié dans le presse-papiers !', 'success'); // on affiche une notification de succès
    }).catch(() => { // si une erreur survient
        showNotification('Erreur lors de la copie', 'error'); // on affiche une notification d'erreur
    });
}

// Initialisation au chargement
document.addEventListener('DOMContentLoaded', function() { // quand le document est chargé
    // Code d'initialisation spécifique à chaque page peut aller ici
    console.log('QuizAI chargé avec succès'); // on affiche un message dans la console
});

// Gère le redimensionnement de la fenêtre
window.addEventListener('resize', function() { // on ajoute un écouteur d'événement au redimensionnement
    // Le redimensionnement peut être géré ici si nécessaire
});

// Prévention de l'envoi de formulaires accidentels
document.addEventListener('keydown', function(e) { // on ajoute un écouteur d'événement au clavier
    if ((e.ctrlKey || e.metaKey) && e.key === 's') { // si Ctrl+S ou Cmd+S est pressé
        e.preventDefault(); // on empêche l'action par défaut
    }
});

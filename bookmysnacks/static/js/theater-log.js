const signIn = document.getElementById('signIn')
const signUp = document.getElementById('signUp')


const fun1 = () => {
    signIn.style.display = 'none'
    signUp.style.display = 'block'
    signUp.setAttribute('aria-hidden', 'false')
    signIn.setAttribute('aria-hidden', 'true')
}

const fun2 = () => {
    signIn.style.display = 'block'
    signUp.style.display = 'none'
    signUp.setAttribute('aria-hidden', 'true')
    signIn.setAttribute('aria-hidden', 'false')
}

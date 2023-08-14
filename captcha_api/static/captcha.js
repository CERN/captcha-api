const captchaApiUrl = "https://captcha.web.cern.ch/api/v1.0";

class CaptchaApiClient {
    baseUrl = captchaApiUrl;

    _formatUrl(relativeUrl) {
        return `${this.baseUrl}/${relativeUrl}`;
    }

    async _request(relativeUrl, options = {}) {
        if (options.method !== "GET") {
        options.headers = { "Content-Type": "application/json" };
        }
        return await (await fetch(this._formatUrl(relativeUrl), options)).json();
    }

    getCaptcha() {
        return this._request("captcha");
    }

    getCaptchaAudioUrl(captchaId) {
        return this._formatUrl(`captcha/audio/${captchaId}`);
    }
}

const Captcha = () => {

    const client = new CaptchaApiClient();
    let captchaResponse;
    let showAudio;

    const reload = async () => {
        captchaResponse = await client.getCaptcha();
        showAudio = false;
        document.getElementById("cern-captcha").innerHTML = template(captchaResponse.id, captchaResponse.img);
        document.getElementById("reload").addEventListener("click", reload);
        document.getElementById("show-audio").addEventListener("click", toggleAudio)
    }

    const toggleAudio = () => {
        showAudio = !showAudio;
        if (showAudio) {
            document.getElementById("audio").innerHTML = audioTemplate(client.getCaptchaAudioUrl(captchaResponse.id));
        } else {
            document.getElementById("audio").innerHTML = "";
        }
        document.getElementById("show-audio").innerText = `${showAudio ? "Hide " : "Show "} audio`;
    }

    const template = (id, img) => `
    <label>Captcha:
    <p>
    The code is valid only for 60 seconds. Your answer will be
    considered incorrect if you don't answer within 60 seconds. You
    can always reset the timer by generating a new code with the "Reload" button below.
    </p>
    <img
    alt="captcha"
    name="captchaResponseImg"
    style="margin-bottom: 4px"
    src="${img}"
    />
    <Button id="reload" type="button">
    Reload
    </Button>
    <Button id="show-audio" type="button">
    Show audio
    </Button>
    <div id="audio"></div>

    <label for="code-input">Code:</label>
    <input
    id="code-input"
    name="captchaAnswer"
    type="text"
    aria-label="Enter code from captcha"
    />
    <input
    name="captchaId"
    type="hidden"
    value="${id}"
    />
    </label>
    `

    const audioTemplate = (audioUrl) => `
    <audio controls="controls" className="audio-element" style="height: 50px">
        <source src="${audioUrl}" />
    </audio>
    `

    reload();
}

document.addEventListener("load", Captcha());

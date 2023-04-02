<template>
	<div>
		<nav>
			<ul>
				<li @click="toggleNotebookDialog()"><strong>Barrel Writer</strong></li>
			</ul>
			<ul>
			    <li><a class="secondary" @click="toggleSettingsDialog()"><strong>settings</strong></a></li>
			    <li><a href="https://github.com/s-m33r/barrel-writer" target="_blank">source</a></li>
			    <li><a href="https://exciting-mercury-836.notion.site/Barrel-An-AI-Based-Writing-Assist-28f61c06f83a4118a2fde1511869bce6" target="_blank">about</a></li>
			</ul>
		</nav>
	</div>

	<!-- NOTEBOOKS DIALOG -->
	<!--
	<dialog open v-show="display_notebooks_page">
		<article>
			<a class="close" @click="toggleNotebookDialog()"></a>

			<a v-for="(notebook, index) in notebooks">notebook {{ index }}</a>
		</article>
	</dialog>
	-->


	<!-- LIST OF PROMPTS AND GENERATIONS FOR SELECTED SESSION -->
	<div
		style="box-shadow: none;"
		v-for="msg in session_history"
	>
		<p style="display: inline;"> {{ msg["prompt"] }}</p>
		<mark style="display: inline;">{{ msg["completion"].slice(msg["prompt"].length + 1) }}</mark>
		<br>
		<a @click="remove(msg)">delete</a>
		<br><br>
	</div>

	<!-- SETTINGS DIALOG -->
	<dialog open v-show="display_settings_page">
		<article>
			<a class="close" @click="toggleSettingsDialog()"></a>

			<blockquote>
			"Words are the model, words are the tools, words are the boards, words are the nails."
			  <footer>
			    <cite>—Richard Rhodes</cite>
			  </footer>
			</blockquote>

			<select id="model" required v-model="model_type">
				<option value="" selected>choose a model</option>
				<option value="scifi">SciFi and Speculative Fiction</option>
  				<option value="litreature">Literary</option>
  				<option value="philosophy">Philosophy</option>
  				<option value="academia">Academia</option>
			</select>

			<label for="output-length">Output Length (10-100 characters)
				<input
					type="range"
					min="10" max="100"
					id="range"
					v-model="generation_length">
			</label>

			<button class="secondary outline" @click="clearSession()">clear notebook</button>
		</article>

	</dialog>

	<!-- MAIN EDITOR -->
	<div>
		<div @keydown.alt.enter="status_waiting_for_response = !status_waiting_for_response; fetch_completion()">
			<textarea id="text-input" v-model="prompt_text">
			</textarea>
		</div>

		<br>
		
		<progress v-show="status_waiting_for_response"></progress>
		<div role="button" class="secondary outline"
			@click="status_waiting_for_response = !status_waiting_for_response; fetch_completion()"
			v-show="!status_waiting_for_response"
		>get suggestion</div>

		<br><br>

		<p style="opacity: 0.5; font-size: 0.6em;">
			<strong>NOTE:</strong><br>Everything you type here is stored locally on your computer. You can clear your notebook by clicking the "clear notebook" button in the settings dialog.<br> This is a proof of concept. The models are not perfect and may generate nonsensical text. Please do not use this for anything serious.
		</p>
	</div>

</template>

<script>
export default {
	data() {
		return {
			display_settings_page: false,
			display_notebooks_page: false,

			status_waiting_for_response: false,

			session_history: [],

			prompt_text: "",
			generation_length: 50,
			model_type: "",
		}
	},

	methods: {
		toggleSettingsDialog() {
			this.display_settings_page = !this.display_settings_page
		},

		toggleNotebookDialog() {
			this.display_notebooks_page = !this.display_notebooks_page
		},

		toggleBoolStatus(status) {
			this[status] = !this[status]
		},

		remove(obj) {
			const index = this.session_history.indexOf(obj);
			if (index > -1) { // only splice array when item is found
				this.session_history.splice(index, 1); // 2nd parameter means remove one item only
			}
		},
		
		async fetch_completion() {
			if (this.input_element.value() == "" || this.model_type == "") {
				if (this.model_type == "") {
					alert("Please select a model from settings")
				}

				this.status_waiting_for_response = false
				return
			}

			const request = new Request("http://localhost:8000/", {
				method: "POST",
				body: JSON.stringify({
					"model": this.model_type,
					"length": parseInt(this.generation_length),
					"prompt": this.input_element.value()
				})
			});

			const response = await fetch(request)

			this.session_history.push(await response.json())
			this.status_waiting_for_response = false
		},

		clearSession() {
			this.session_history = []
		}

	},

	mounted() {
		// Set up SimpleMDE editor
		this.input_element = new SimpleMDE({
			autofocus: true,
			element: document.getElementById("text-input"),
			autosave: {
				enabled: true,
				uniqueId: "simpleMDE_autosave_data",
				delay: 1000,
			},

			spellChecker: false,
			toolbar: false,
			status: false,

			placeholder: "Type here...\nPress Alt+Enter to get a suggestion (or click the button below)"
		})

		/*
		// load notebooks from LocalStorage, create if doesn't exit
		if (localStorage.getItem("notebooks") == null) {
			localStorage.setItem("notebooks", JSON.stringify(this.session_history))
		} else {
			this.session_history = JSON.parse(localStorage.getItem("notebooks"))
		}
		*/
	},

	beforeUnmount() {
		/*
		// save notebooks to LocalStorage
		localStorage.setItem("notebooks", JSON.stringify(this.session_history))
		*/
	}

}
</script>

<style>
/* minimum height of editor (SimpleMDE) */
.CodeMirror, .CodeMirror-scroll {
	min-height: 100px;
}
</style>

"use strict";

window.addEventListener("load", () => {
  window.history.pushState({ page: 1 }, "", window.location.href);
});

///////////////////////////////////////////////////////////
// get the url from the id of the button clicked
const getUrl = (eventTargetId, tweetId) => {
  switch (eventTargetId) {
    case "feed":
      return "/";
    case "profile":
      return "/profile";
    case "new-tweet":
    case "submit-new-tweet":
      return "/tweets/new";
    case "sign-up":
    case "submit-sign-up":
      return "/signup";
    case "log-out":
    case "log-in":
      return "/login";
    case "edit-tweet":
    case "submit-edit-tweet":
      if (tweetId === undefined) return "/";
      return "/tweets/edit/" + tweetId;
    case "delete-tweet":
      if (tweetId === undefined) return "/";
      return "/tweets/delete/" + tweetId;
    default:
      return "/";
  }
};

///////////////////////////////////////////////////////////
// set the content of the html document based on response
const setHTML = async (response, event) => {
  await response.text().then((responseText) => {
    // get the html content from the response text
    const content = responseText.slice(
      responseText.indexOf('<html lang="en">') + '<html lang="en">'.length,
      responseText.indexOf("</html>") - "</html>".length
    );

    // set the html to the content
    document.querySelector("html").innerHTML = content;

    if (response.url !== window.location.href) {
      // update url (with errors in query string or whatever page it's been redirected to)
      window.history.pushState(null, null, response.url);
    }
  });
};

////////////////////////////////////////////////////////////
// fetches and returns response based on variables passed
const fetchResponse = async (method, url, form) => {
  // set method and form if relevant
  const init = {
    method: method,
  };
  if (form) {
    init["body"] = new FormData(form);
  }

  // fetch and return response
  const response = await fetch(url, init);
  return response;
};

////////////////////////////////////////////////////////////
// called on buttons, navigation, form submits, etc.
const handleNavigation = async (event, method = "GET") => {
  let form = undefined;
  let tweetId = undefined;
  if (event.type !== "popstate") {
    event.preventDefault();
    event.stopPropagation();

    form = event.target.form ? event.target.form : undefined;
    tweetId = form && form.dataset.tweetId ? form.dataset.tweetId : undefined; // used for editing and deleting tweets
  }
  // fetch
  await fetchResponse(
    method, // method
    event.type !== "popstate"
      ? getUrl(event.target.id, tweetId)
      : window.location.pathname, // url based on event's target's id
    method !== "GET" && form !== undefined ? form : undefined // form if method isn't get or delete
  ).then((response) => {
    // check response
    if (!response.ok) {
      window.location = "/";
      return;
    }
    // get response as text and insert html
    setHTML(response, event);
  });
};

////////////////////////////////////////////////////////////////
// handle clicking 'back' in the browsers
window.addEventListener("popstate", (event) => handleNavigation(event));

////////////////////////////////////////////////////////////////
// remove image from file input when editing or creating tweets
const removeImage = (event) => {
  event.preventDefault();
  event.stopPropagation();

  // when removing an image from editing a tweet
  const image = event.target.form.querySelector("#tweet_image_name");
  if (image && image.value !== "") {
    // remove image
    image.value = "remove";
    // hide the image input
    event.target.form.querySelector("#remove_image").classList.add("hidden");
    // show the add image input
    event.target.form
      .querySelector("#add-new-image")
      .classList.remove("hidden");
  }

  // when removing image from file upload input
  const image_file = event.target.form.querySelector("#tweet_image");
  if (image_file) {
    image_file.value = "";
  }
};

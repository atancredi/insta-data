const userQueryRes = await fetch(
    `https://www.instagram.com/web/search/topsearch/?query=${username}`
);

const userQueryJson = await userQueryRes.json();
return userQueryJson.users[0].user.pk;
l <- read.csv('~/Dropbox/GenreProject/python/reception/poetry/logisticpredictions.csv')
l$birthdate[l$birthdate < 1700] <- NA
l$reviewed[l$reviewed == 'addedbecausecanon'] <- NA
model = glm(data = l, formula = as.integer(reviewed == 'rev') ~ logistic + pubdate, family = binomial(logit))
intercept = coef(model)[1] / (-coef(model)[2])
slope = coef(model)[3] / (-coef(model)[2])
line = intercept + (slope * l$pubdate)
true = sum(l$logistic > line & l$reviewed == 'rev', na.rm = TRUE) + sum(l$logistic <= line & l$reviewed == 'not', na.rm = TRUE)
false = sum(l$logistic < line & l$reviewed == 'rev', na.rm = TRUE) + sum(l$logistic >= line & l$reviewed == 'not', na.rm = TRUE)
print(true / (true + false))
levels(l$reviewed) = c('random', 'reviewed')
hemans <- filter(l, author == 'Hemans,')

p <- ggplot(l, aes(x = pubdate, y = logistic, color = reviewed, shape = reviewed)) + 
  geom_point() + geom_abline(intercept = intercept, slope = slope) + scale_shape(name="actually") +
  geom_line(data = hemans, show_guide = FALSE) +
  scale_color_manual(name = "actually", values = c('gray64', 'red3')) + 
  theme(text = element_text(size = 16)) + 
  scale_y_continuous('Predicted probability of coming from reviewed set\n', labels = percent) + 
  ggtitle('170 volumes of poetry before 1860.\n') + scale_x_continuous("")
plot(p)
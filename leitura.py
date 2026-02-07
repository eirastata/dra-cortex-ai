from service.vetorizacao import vetorizar, encode_y


if __name__ == "__main__":

    X, vec = vetorizar()
    y, enc = encode_y()

    print("Formato X:", X.shape)
    print("Primeiros y:", y[:10])
    print("Classes:", enc.classes_)
